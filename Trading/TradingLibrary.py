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
        tokendata = coinbasedatasearching.gettimeframecoinbasetoken(Token=token, TimeFrame=4)
        # Now run this data through algorithm one
        outcome = algorithmone.algorithmone(tokendata, Tolerance)
        recordrecommendation(outcome)
    ############ Binance ############
    # For Binance, given the much greater efficacacy of data, will need to take a different approach
    # Get a list of unique binance tokens available to search
    binancelist = binancedatasearching.getuniquebinancetokens()
    # Get the lenght of this list to analyze efficiency of search
    binancenum = len(binancelist)
    # Now get a dataframe of ALL binance data from past four hours
    binancedata = binancedatasearching.gettimeframealltokens(4)
    # For each token in the list of coinbase tokens, run through algorithm one
    for token in binancelist:
        # Slice binance data into a smaller chunk
        tokendata = binancedata[binancedata.Token.eq(token)]
        # Now analyse smaller dataframe
        outcome = algorithmone.algorithmone(tokendata, Tolerance)
        # Record the recommendation
        recordrecommendation(outcome)

    end = timer()
    timetaken = end - start
    totaltokens = coinbasenum + binancenum
    logging.info(f'Algorithm one completed on {totaltokens} tokens, total time taken (in seconds): {timetaken}')

# Insert the trading recommendation into Database collection
def recordrecommendation(Data):
    record = mongodb.insertsingleintotradingrecommendations(Data)
    return record