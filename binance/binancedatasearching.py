from datamunging import genericdatamunging
from databasing import mongodb
import logging
import datetime

# Library for searching binance data

# Get a single token from binance data
def getbinancetoken(Token):
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(process)d - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO, filename='app.log', filemode='a')
    # Make sure token is a string
    Token = str(Token)
    # Log action
    logging.info(f'Getting info from binance database for {Token}')
    # Construct the query to be passed to mongo search
    Query = {'symbol': Token}
    outcome = genericdatamunging.getlastbinancepricedata(Query)
    return outcome

# Get a list of unique token values from coinbase
def getuniquebinancetokens():
    outcome = mongodb.getuniquebinancetokens()
    return outcome

# Get a single token scoped to a specific timeframe for search. Timeframe must be in hours
def gettimeframebinancetoken(Token, TimeFrame):
    # Take TimeFrame and get the period of time this represents
    time = str(datetime.datetime.now() - datetime.timedelta(hours=TimeFrame))
    # Construct the query to pass to MongoDb
    Query = {'symbol': Token, 'DateTimeGathered': {'$gt': time}}
    # Search database for this query
    outcome = genericdatamunging.getlastbinancepricedata(Query)
    return outcome

# Scope down the columns received from search to make faster
def gettimeframescopedbinancetoken(Token, TimeFrame):
    # Take TimeFrame and get the period of time this represents
    time = str(datetime.datetime.now() - datetime.timedelta(hours=TimeFrame))
    # Construct the query to pass to MongoDb
    Query = {'symbol': Token, 'DateTimeGathered': {'$gt': time}, 'Exchange': 1, 'lastPrice': 1}
    # Search database for this query
    outcome = genericdatamunging.getlastbinancepricedata(Query)
    return outcome

# Function to get a list of all tokens from past 4 hours with binance
def gettimeframealltokens(TimeFrame):
    # Take TimeFrame and get the period of time this represents
    time = str(datetime.datetime.now() - datetime.timedelta(hours=TimeFrame))
    # Construct the query to pass to MongoDb
    Query = {'DateTimeGathered': {'$gt': time}}
    # Search database for this query
    outcome = genericdatamunging.getlastbinancepricedata(Query)
    return outcome

