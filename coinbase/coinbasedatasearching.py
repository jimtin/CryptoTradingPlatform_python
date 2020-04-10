from datamunging import genericdatamunging
from databasing import mongodb
import datetime

# Library for retrieving coinbase data from database

# Get a single token from coinbase data
def getcoinbasetoken(Token):
    # Make sure token is a string
    Token = str(Token)
    # Construct the query to be passed to mongo search
    Query = {'base': Token}
    # Search database for this query
    outcome = genericdatamunging.getlastcoinbasepricedata(Query)
    return outcome


# Get a list of unique token values from coinbase
def getuniquecoinbasetokens():
    outcome = mongodb.getuniquecoinbasetokens()
    return outcome


# Get a single token from a period of time calculated backwards
def getlatestcoinbasetoken(Token, TimeFrame):
    # Take TimeFrame and get the period of time this represents
    StartTime = datetime.datetime.now()
    EndTime = datetime.datetime.now() - datetime.timedelta(hours=TimeFrame)
    # Pass query into gettokenovertimeframe
    outcome = gettokenovertimeframe(Token, StartTime, EndTime)
    return outcome


# Get a single token between certain timeframes
def gettokenovertimeframe(Token, StartTime, EndTime):
    # Turn StartTime and EndTime into strings
    StartTime = str(StartTime)
    EndTime = str(EndTime)
    # Set up the query
    query = {'base': Token, 'DateTimeGathered': {'$gte': StartTime, '$lte': EndTime}}
    outcome = genericdatamunging.getcoinbasepricedata(query)
    return outcome


