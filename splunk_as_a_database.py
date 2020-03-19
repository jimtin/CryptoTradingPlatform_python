import socket
from pathlib import Path
import json
from time import sleep
import xmltodict
import requests
from requests.auth import HTTPBasicAuth
import urllib3


# Use Splunks REST API as a database

# FilePath = input("Input FilePath for Splunk settings")

# Put the data from Binance into a database for future post processing
# Create a simple UDP sender. There is nothing secret about the data, so sending in the clear is fine
def splunkudpsender(datatosend, splunksettings):
    # First, import splunk settings
    SplunkIP = splunksettings["SplunkIP"]
    SplunkPort = int(splunksettings["SplunkPort"])
    # Now convert the message to bytes
    MESSAGE = str.encode(datatosend)
    # Set up the socket to send (btw, how good is python)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Send datagram (UDP)
    sock.sendto(MESSAGE, (SplunkIP, SplunkPort))
    sock.close()
    sleep(0.01)


# Get splunk settings so I know where to send data
def getsplunksettings(FilePath):
    FilePath = str(FilePath)
    filepath = Path(FilePath)
    f = open(filepath)
    splunksettingsjson = f.read()
    splunksettings = json.loads(splunksettingsjson)
    return splunksettings["SplunkSettings"]


# Query Splunk to get information
def querysplunk(SearchQuery, FilePath, sessionkey=""):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Ensure that SearchQuery is a string
    SearchQuery = str(SearchQuery)
    # Get splunk settings
    splunksettings = getsplunksettings(FilePath)
    # Set up base API
    apirequest = splunksettings["BaseURL"] + "/services/search/jobs/"
    # If a session key provided, use it, otherwise get it
    if sessionkey == "":
        # Get the session key
        sessionkey = getsplunksessionkey(FilePath)
    else:
        sessionkey = sessionkey
    data = {
        "search": SearchQuery,
        "ouput_mode": "json"
    }
    session = requests.session()
    session.headers.update({'Authorization': 'Splunk ' + sessionkey})
    information = session.post(apirequest, data=data, verify=False)
    # The information returned is in xml, and I really just want the sessionkey, so convert
    information = xmltodict.parse(information.text)
    sid = information['response']['sid']
    # Now get the search results
    results = getsearchresults(sid, sessionkey, splunksettings)
    return results


# Function to get search results from Splunk
def getsearchresults(sid, sessionkey, splunksettings):
    # Set up the session
    session = requests.session()
    # Update headers
    session.headers.update({'Authorization': 'Splunk ' + sessionkey})
    # Now set up the data that we want
    # Set up the api request to get the results. Use the Search ID (sid)
    # Had issues using the data parameter for requests, so put into search string manually
    apirequest = splunksettings["BaseURL"] + "/services/search/jobs/" + sid + "/results/?count=0&output_mode=json"
    # This is a get request
    information = session.get(apirequest, verify=False)
    # If response code 204 returns, assume search is not complete, so try next time
    #print("Status Code: " + str(information.status_code))
    while information.status_code == 204:
        #print("Results not yet complete, trying again")
        information = session.get(apirequest, verify=False)
        #print("Status Code: " + str(information.status_code))
        sleep(5)
    #print("Results received")
    # Take the string and turn it into a json object
    results = json.loads(information.text)
    # Return results
    return results["results"]

# Query Splunk to get any messages
def getsplunkmessages(FilePath):
    # Set up the api query
    apirequest = "https://localhost:8089/services/messages"
    # Get Splunk Settings
    splunksettings = getsplunksettings(FilePath)
    # Set up the session
    session = requests.session()
    information = requests.get(apirequest, auth=HTTPBasicAuth(str(splunksettings["UserName"]), str(splunksettings["Password"])), verify=False)
    return information.text


# Query Splunk to get a session key, this can be used to secure comms afterwards
def getsplunksessionkey(FilePath):
    # Get Splunk Settings
    splunksettings = getsplunksettings(FilePath)
    # Set up the api query
    apirequest = "https://localhost:8089/services/auth/login"
    # The Splunk REST API requires the username and password to be URL encoded. However, Python Requests does this when it's turned into a dictionary
    session = requests.session()
    data={"username": splunksettings["UserName"], "password":splunksettings["Password"]}
    information = session.get(apirequest, data=data, verify=False)
    # The data returned is in xml format, so convert into a dictionary
    information = xmltodict.parse(information.text)
    return information['response']['sessionKey']


# Function to send data to Splunk and include the exchange it is from
def sendtosplunk(data, exchange, splunksettings):
    # Ensure the exchange is a string
    exchange = str(exchange)
    # Iterate through the data provided, adding in the exchange
    for crypto in data:
        # Add in the exchange
        # print(crypto)
        crypto.update({'exchange': exchange})
        crypto.update({'DateTime': str(datetime.datetime.now())})
        # Turn into json
        exchangedata = json.dumps(crypto)
        # Serialize the crypto object into a string
        exchangedata = str(exchangedata)
        # Now send joyfully to Splunk
        splunkudpsender(exchangedata, splunksettings)

