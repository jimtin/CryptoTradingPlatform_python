import pandas
from datamunging import genericdatamunging
from databasing import mongodb

# Library for retrieving coinbase data from database

# Get a single token from coinbase data
def getcoinbasetoken(Token):
    # Make sure token is a string
    Token = str(Token)
    # Construct the query to be passed to mongo search
    Query = {'base': Token}
    outcome = genericdatamunging.getlastcoinbasepricedata(Query)
    return outcome

# Get a list of unique token values from coinbase
def getuniquecoinbasetokens():
    outcome = mongodb.getuniquecoinbasetokens()
    return outcome


