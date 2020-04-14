from coinbase import coinbasedatasearching
from TradingAlgorithms import algorithmone
from databasing import mongodb
from binance import binancedatasearching
from timeit import default_timer as timer
from Trading import TradingFunctions
from selfanalysis import logginglibrary
import time
from datamunging import genericdatamunging
import pandas
import numpy

# Library to implement trading algorithms

# Implment algorithm one
def implementalgorithmone(Tolerance):
    # Algorithm one is a moving average analysis
    # Start the timer on the algorithm
    start = timer()
    # Get a list of coinbase tokens
    coinbaselist = coinbasedatasearching.getuniquecoinbasetokens()
    coinbasenum = len(coinbaselist)
    # For each token in the list of coinbase tokens, run through algorithm one
    for token in coinbaselist:
        # First get the data for each token
        tokendata = coinbasedatasearching.getlatestcoinbasetoken(Token=token, TimeFrame=4)
        # Now run this data through algorithm one
        outcome = algorithmone.algorithmonebuy(tokendata, Tolerance)
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
        outcome = algorithmone.algorithmonebuy(tokendata, Tolerance)
        # Record the recommendation
        recordrecommendation(outcome)
        # If recommendation is to purchase, pass to function to do so
        if outcome["Recommendation"] == "Buy":
            TradingFunctions.purchasetoken(Token=token, Exchange="binance")
    # Capture the end of the function
    end = timer()
    # Calculate the time taken
    executetime = end - start
    # Calculate the total number of coins analysed
    totaltokens = coinbasenum + binancenum
    logginglibrary.logalgorithmselfanalysisevents("AlgorithmOne", executetime, totaltokens, "implementalgorithmone")


# Insert the trading recommendation into Database collection
def recordrecommendation(Data):
    record = mongodb.insertsingleintotradingrecommendations(Data)
    return record

# Function to keep interating through a list of algorithms
def iteralgorithms(Tolerance=0.5, Start=False):
    while Start==True:
        try:
            implementalgorithmone(Tolerance)
        except:
            print("Algorithm One error observed")
            time.sleep(30)

# Function to wargame algorithm one
# Desire is to take algorithm one and run over historical data. Over time this will allow for more efficient and effective trading
def testcoinbasealgorithmonetolearnaces(Token, InvestmentAmount):
    # Start a timer on the function so it can be measured
    start = timer()
    # Get all the entries for a single coinbase Token
    # First construct the query to be passed
    query = {'base': Token}
    # Query database
    TokenDataFrame = genericdatamunging.getcoinbasepricedata(query)
    # Get the start time of data
    startime = TokenDataFrame.head(1).index.values[0]
    # Get the stop time of the data
    endtime = TokenDataFrame.tail(1).index.values[0]
    # Get the time range this will be over
    timerange = int(endtime - startime)
    # Get a range of different time slices for future use
    seconds = timerange/1e9
    minutes = timerange/(1e9*60)
    hours = timerange/(1e9 * 60 * 60)
    days = timerange/(1e9 * 60 * 60 * 24)
    # Define what success is
    # Get start price
    startprice = TokenDataFrame.head(1).Price.values[0]
    # Get end price
    endprice = TokenDataFrame.tail(1).Price.values[0]
    # Get the delta
    change = endprice - startprice
    # Calculate the number of units which would have been bought with the investment amount
    numunits = InvestmentAmount/startprice
    # Multiply this against the change
    successcriteria = numunits * change
    print(f'Success Amount to beat is: ${successcriteria}')
    # Set up a list to store outcomes while testing
    analysisresults = []
    # Set up a for loop to iterate through dataframe using 1 minute intervals
    # First calculate the maximum value. This will 5 hours less than the end time
    stoptime = endtime - numpy.timedelta64(5, 'h')
    dfstarttime = startime
    while dfstarttime < stoptime:
        # Using dfstarttime, get the end time. This will be five hours from start time
        dfendtime = dfstarttime + numpy.timedelta64(5, 'h')
        # To confirm my sanity, print the start and end times
        # Now select a five hour window from DataFrame
        # First transform dfstarttime and dfendtime into strings
        dfstarttimestring = str(dfstarttime)
        dfendtimestring = str(dfendtime)
        # Select the slice of the Dataframe, store in a separate dataframe. Have wrapped in a try statement while I deal with not enough data errors
        try:
            analysisdf = TokenDataFrame.loc[dfstarttimestring:dfendtimestring]
            # Run through algorithm. Tolerance hardcoded in while exploring data
            outcome = algorithmone.algorithmonebuy(analysisdf, Tolerance=0.1)
            if outcome["Recommendation"] == "Buy":
                print(outcome["Recommendation"])
            # Store results
            analysisresults.append(outcome)
        except:
            error = "Error"
        # Now add one minute to dfstarttime
        dfstarttime = dfstarttime + numpy.timedelta64(1, 'm')

    # todo: combine the two calculations together to see if I can 'buy' and 'sell' based upon criteria
    # todo: store the outcomes into separate database
    # todo: using this, iterate through entire list of tokens and develop custom trading amounts for each token
    # todo: iterate in 0.1% amounts plus / minus
    # Potential considerations:
    # 1. Symmetrical vs non-symmetrical limits. i.e. if it rises by 1% should the exit also be 1%
    # 2. Amounts. Should all of the Investment Amount be invested, or is the risk lowered if the amount is decreased?
    end = timer()
    timetaken = end - start
    print(f"Time taken on algorithm was {timetaken}")
    return analysisresults

# Function to pass all coinbase tokens through coinbase algorithm testing
def testallcoinbasetokens():
    # Get a list of coinbase tokens
    coinbaselist = coinbasedatasearching.getuniquecoinbasetokens()
    coinbasenum = len(coinbaselist)
    for token in coinbaselist:
        print(f'Now testing {token}')
        result = testcoinbasealgorithmonetolearnaces(token, 10000)
