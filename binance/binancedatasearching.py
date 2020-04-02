from datamunging import genericdatamunging
from databasing import mongodb
import logging

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

