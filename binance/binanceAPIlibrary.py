import requests
import time
import hmac
import hashlib
import json
import datetime

# test the binance api to see if it's working.
def binanceapiinit():
    # Basic request to check if binance wapi is up and running. From this website: https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md
    api = requests.get('https://www.binance.com/wapi/v3/systemStatus.html')
    # If the status code is 200, will confirm that the binance api is up and working
    if api.status_code == 200:
        statusjson = api.text
        # Convert JSON into a dictionary
        status = json.loads(statusjson)
        # This confirms that Binance API is up and running
        if status['status'] == 0:
            print("Binance API ready to accept requests")
            return True
        # This confirms that Binance API is undergoing maintenance
        elif status['status'] == 1:
            print("Binance API undergoing maintenance")
            return False
    else:
        print("Binance API does not work")
        return False


# Function to create the HMAC signature for Binance
def createbinancehmac256(querystring, secretKey):
    # Now create a HMAC SHA256 signature
    secret_key = str.encode(secretKey)
    total_params = str.encode(querystring)
    hmacsignature = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
    # Print new hmac signature just for checking
    # print("HMAC Sig: " + hmacsignature)
    return hmacsignature


# Function to get the account status of a user
def getaccountstatus(PublicKey, secretkey):
    apirequest = "https://www.binance.com/wapi/v3/accountStatus.html?"
    # Get timestamp of request
    timestamp = str(int(round(time.time() * 1000)))
    timestampstring = "timestamp=" + timestamp
    # Now create the HMAC key
    # HMAC only needs timestamp in params, so pass timestamp string to it
    hmacsig = createbinancehmac256(timestampstring, secretkey)
    hmacsig = str(hmacsig)
    # Now concatenate the timestampstring and apirequest together for requester URL without HMAC
    apirequest = apirequest + timestampstring
    accountstatus = queryauthenticatedbinance(PublicKey, apirequest, hmacsig)
    return accountstatus


# Function to use HMAC etc to query the Binance api
def queryauthenticatedbinance(PublicKey, querystring, HMAC):
    # Set up python session
    session = requests.session()
    session.headers.update({'Accept': 'application/json', 'X-MBX-APIKEY': PublicKey})
    # Display the query being made
    print("##############################")
    print("Binance API being queried:")
    print(querystring)
    querystring = querystring + "&signature=" + HMAC
    information = session.get(querystring)
    print("##############################")
    return information.text


# Get withdrawal history from binance for a set user
def getwithdrawalhistory(PublicKey, secretkey):
    # Setup the request
    apirequest = "https://www.binance.com/wapi/v3/withdrawHistory.html?"
    # Get timestamp of request
    timestamp = str(int(round(time.time() * 1000)))
    timestampstring = "timestamp=" + timestamp
    # Now create the HMAC key
    # HMAC only needs timestamp in params, so pass timestamp string to it
    hmacsig = createbinancehmac256(timestampstring, secretkey)
    hmacsig = str(hmacsig)
    # Now concatenate the timestampstring and apirequest together for requester URL without HMAC
    apirequest = apirequest + timestampstring
    # Notify user of new list of withdrawals coming through
    print("##############################")
    print("New list of withdrawals printing to screen")
    withdrawalhistoryjson = queryauthenticatedbinance(PublicKey, apirequest, hmacsig)
    # Now print a list of the trades for tracking purposes
    # First convert in dict
    withdrawalhistory = json.loads(withdrawalhistoryjson)
    print("##############################")
    return withdrawalhistory


# Get deposit history for a user
def getdeposithistory(PublicKey, secretkey):
    apirequest = "https://www.binance.com/wapi/v3/depositHistory.html?"
    # Get timestamp of request
    timestamp = str(int(round(time.time() * 1000)))
    timestampstring = "timestamp=" + timestamp
    # Now create the HMAC key
    # HMAC only needs timestamp in params, so pass timestamp string to it
    hmacsig = createbinancehmac256(timestampstring, secretkey)
    hmacsig = str(hmacsig)
    # Now concatenate the timestampstring and apirequest together for requester URL without HMAC
    apirequest = apirequest + timestampstring
    # Notify user of new list of deposits coming through
    deposithistoryjson = queryauthenticatedbinance(PublicKey, apirequest, hmacsig)
    # Now print a list of the trades for tracking purposes
    print("##############################")
    print("New list of deposits printing to screen")
    # First convert in dict
    deposithistory = json.loads(deposithistoryjson)
    print(deposithistory)
    #for item in deposithistory
    print("##############################")
    return deposithistory


# Use rest API to query open orders
def getallopenorders(PublicKey, secretkey):
    # Note this is the REST API, not wapi
    apirequest = "https://api.binance.com/api/v3/openOrders?"
    # Get timestamp of request
    timestamp = str(int(round(time.time() * 1000)))
    timestampstring = "timestamp=" + timestamp
    # Now create the HMAC key
    # HMAC only needs timestamp in params, so pass timestamp string to it
    hmacsig = createbinancehmac256(timestampstring, secretkey)
    hmacsig = str(hmacsig)
    # Now concatenate the timestampstring and apirequest together for requester URL without HMAC
    apirequest = apirequest + timestampstring
    # Store returned result from queryauthenticated binance
    openordersjson = queryauthenticatedbinance(PublicKey, apirequest, hmacsig)
    # Print results to screen
    print("##############################")
    print("Currently open orders: ")
    openorders = json.loads(openordersjson)
    print(openorders)
    print("##############################")
    return openorders


# Get information about the account
def getaccountinfo(PublicKey, secretkey):
    # Note this uses the REST API, not wapi https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
    apirequest = "https://api.binance.com/api/v3/account?"
    # Get timestamp of request
    timestamp = str(int(round(time.time() * 1000)))
    timestampstring = "timestamp=" + timestamp
    # Now create the HMAC key
    # HMAC only needs timestamp in params, so pass timestamp string to it
    hmacsig = createbinancehmac256(timestampstring, secretkey)
    hmacsig = str(hmacsig)
    # Now concatenate the timestampstring and apirequest together for requester URL without HMAC
    apirequest = apirequest + timestampstring
    # Store returned result from queryauthenticated binance
    accountinfojson = queryauthenticatedbinance(PublicKey, apirequest, hmacsig)
    # Convert into json array
    accountinfo = json.loads(accountinfojson)
    print("##############################")
    print("Account Info:")
    print(accountinfo)
    print("##############################")
    return accountinfo


# Get trading information about the account
def getexchangeinfo():
    apirequest = "https://api.binance.com/api/v3/exchangeInfo"
    # No parameters or authentication required, so can use a simple python request
    session = requests.session()
    session.headers.update({'Accept': 'application/json'})
    information = session.get(apirequest)
    exchangeinfojson = information.text
    exchangeinfo = json.loads(exchangeinfojson)
    return exchangeinfo


# Return exchange information to the screen in a more human readable format
def getexchangeinfohumanreadable():
    exchangeinfo = getexchangeinfo()
    symbols = exchangeinfo["symbols"]
    for crypto in symbols:
        print(crypto["symbol"], crypto["baseAsset"])


# Get information about the depth of the market
def getmarketdepth(PublicKey, symbol, limit=500):
    apirequest = "https://api.binance.com/api/v3/depth"
    # Turn limit into a string
    limit = str(limit)
    # Construct the full api request
    apirequest = apirequest + "?symbol=" + symbol + "&limit=" + limit
    # The MarketData endpoint requires the PublicKey to work, however, no signature
    session = requests.session()
    session.headers.update({'Accept': 'application/json', 'X-MBX-APIKEY': PublicKey})
    # Get market depth from binance
    information = session.get(apirequest)
    # Convert into json
    marketdepth = json.loads(information.text)
    return marketdepth


# Get a list of the recent trades which were made
def getrecenttrades(PublicKey, symbol, limit=500):
    apirequest = "https://api.binance.com/api/v3/trades"
    # Turn limit into a string
    limit = str(limit)
    # Construct the full api request
    apirequest = apirequest + "?symbol=" + symbol + "&limit=" + limit
    # The MarketData endpoint requires the PublicKey to work, however, no signature
    session = requests.session()
    session.headers.update({'Accept': 'application/json', 'X-MBX-APIKEY': PublicKey})
    # Get recent trades from binance
    information = session.get(apirequest)
    # Convert into json
    recenttrades = json.loads(information.text)
    return recenttrades


# Get 24 hour price change statistics for specified symbols
def getpricechanges(symbol="ALL"):
    apirequest = "https://api.binance.com/api/v3/ticker/24hr"
    # Construct the apirequest based upon symbol provided
    if symbol == "ALL":
        apirequest = apirequest
    else:
        apirequest = apirequest + "&symbol=" + symbol
    session = requests.session()
    # Get 24 hour price change statistics for specified symbols
    information = session.get(apirequest)
    # Convert into json
    pricechange = json.loads(information.text)
    return pricechange


