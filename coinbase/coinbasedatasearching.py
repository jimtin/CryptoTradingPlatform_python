from datamunging import genericdatamunging
from databasing import mongodb
import logging

# Library for retrieving coinbase data from database

# Get a single token from coinbase data
def getcoinbasetoken(Token):
    # Set up logger
    logging.basicConfig(format='%(asctime)s - %(process)d - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO, filename='app.log', filemode='a')
    logging.info(f'Getting info from coinbase database for {Token}')
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


