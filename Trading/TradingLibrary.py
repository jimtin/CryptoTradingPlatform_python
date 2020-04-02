from coinbase import coinbasedatasearching
from TradingAlgorithms import algorithmone
from databasing import mongodb
from binance import binancedatasearching
from timeit import default_timer as timer
import logging

# Library to implement trading algorithms

# Implment algorithm one
def implementalgorithmone(Tolerance=2):
    # Algorithm one is a moving average analysis
    # Start the timer on the algorithm
    start = timer()
    print(start)
    # Set up the logger
    logging.basicConfig(format='%(asctime)s - %(process)d - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO, filename='app.log', filemode='a')
    logging.info("Starting algorithm one")
    # Get a list of coinbase tokens
    coinbaselist = coinbasedatasearching.getuniquecoinbasetokens()
    coinbasenum = len(coinbaselist)
    # For each token in the list of coinbase tokens, run through algorithm one
    for token in coinbaselist:
        # First get the data for each token
        tokendata = coinbasedatasearching.getcoinbasetoken(Token=token)
        # Now run this data through algorithm one
        outcome = algorithmone.algorithmone(tokendata, Tolerance)
        recordrecommendation(outcome)
    ############ Binance ############
    binancelist = binancedatasearching.getuniquebinancetokens()
    binancenum = len(binancelist)
    # For each token in the list of coinbase tokens, run through algorithm one
    for token in binancelist:
        # First get the data for each token
        tokendata = binancedatasearching.getbinancetoken(Token=token)
        outcome = algorithmone.algorithmone(tokendata, Tolerance)
        print(outcome)
        recordrecommendation(outcome)

    end = timer()
    timetaken = end - start
    totaltokens = coinbasenum + binancenum
    logging.info(f'Algorithm one completed on {totaltokens} tokens, total time taken (in seconds): {timetaken}')

# Insert the trading recommendation into Database collection
def recordrecommendation(Data):
    record = mongodb.insertsingleintotradingrecommendations(Data)
    return record