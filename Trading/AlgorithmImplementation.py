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
import datetime
import sys

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
# todo: store the outcomes into separate database
# todo: using this, iterate through entire list of tokens and develop custom trading amounts for each token
# todo: iterate in 0.1% amounts plus / minus


# Function to get a list of all the coinbase tokens
def getallcoinbasetokens():
    # Start timer on function
    start = timer()
    # Get a list of coinbase tokens
    coinbaselist = coinbasedatasearching.getuniquecoinbasetokens()
    # Get a count of the number of tokens
    numtokens = len(coinbaselist)
    # Finish timer
    end = timer()
    # Calculate time taken
    timetaken = end - start
    # Put results in a dictionary for future analysis
    outcomedict = {
        "TimeTaken": timetaken,
        "UniqueCoinbaseTokens": coinbaselist,
        "NumberofTokens": numtokens
    }
    return outcomedict


# Function to get a list of all the binance tokens
def getallbinancetokens():
    # Start timer on function
    start = timer()
    # Get a list of coinbase tokens
    binancelist = binancedatasearching.getuniquebinancetokens()
    # Get a count of the number of tokens
    numtokens = len(binancelist)
    # Finish timer
    end = timer()
    # Calculate time taken
    timetaken = end - start
    # Put results in a dictionary for future analysis
    outcomedict = {
        "TimeTaken": timetaken,
        "UniqueBinanceTokens": binancelist,
        "NumberofTokens": numtokens
    }
    return outcomedict


# Create generic algorithm one test function. Assume TokenDataFrame has been passed through generic datamunging so data is consistent
def testalgorithmone(TokenDataFrame, InvestmentAmount, BuyTolerance, SellTolerance):
    # Start the timer on the function
    start = timer()
    # Create the results dictionary
    result = {
        "Token": "",
        "Exchange": "",
        "InvestmentAmount": InvestmentAmount,
        "BuyTolerance": BuyTolerance,
        "SellTolerance": SellTolerance,
        "HODLOutcome": 0,
        "HoursAnalysed": 0,
        "BuyRecommendations": 0,
        "SellRecommendations": 0,
        "AlgorithmCash": 0,
        "ProfitLoss": 0,
        "AlgorithmOutcome": "",
        "Key": "testalgorithmone",
        "DateTime": str(datetime.datetime.now()),
        "IndexError": 0
    }
    # Get the Token name, store in dictionary
    tokenname = TokenDataFrame.tail(1).Token.values[0]
    result["Token"] = tokenname
    # Get the Exchange, store in dictionary
    tokenexchange = TokenDataFrame.tail(1).Exchange.values[0]
    result["Exchange"] = tokenexchange
    # Figure out what success would look like (HODL)
    startprice = TokenDataFrame.head(1).Price.values[0]
    result["TokenStartPrice"] = startprice
    endprice = TokenDataFrame.tail(1).Price.values[0]
    result["TokenEndPrice"] = endprice
    pricechange = endprice - startprice
    result["TokenPriceChange"] = pricechange
    HODLOutcome = (pricechange * InvestmentAmount) + InvestmentAmount
    result["HODLOutcome"] = HODLOutcome
    # Get start and end times of TokenDataFrame
    startime = TokenDataFrame.head(1).index.values[0]
    stoptime = TokenDataFrame.tail(1).index.values[0]
    # Get number of hours analysed (will assist with efficiency calculations later)
    timerange = int(stoptime - startime)
    hours = timerange / (1e9 * 60 * 60)
    result["HoursAnalysed"] = hours
    # Determine the time to stop iteration without getting out of range
    endtime = stoptime - numpy.timedelta64(5, 'h')
    # Clone startime variable to enable comparative operator
    dfstartime = startime
    # Set a variable to indicate if a buy or sell is required. All instances start with a buy recommendation
    buyorsell = "buy"
    # Set the initial buy at zero
    numtokenspurchased = 0
    # Setup the variable to record the number of buy recommendations
    buyrecommendations = 0
    # Setup the variable to record the number of sell recommendations
    sellrecommendations = 0
    # Set a variable to track cashonhand. Initially starts with the investment amount
    cashonhand = InvestmentAmount
    while dfstartime < endtime:
        # Set the end time of this particular dataframe slice. This will be five hours.
        dfendtime = dfstartime + numpy.timedelta64(5, 'h')
        # Slice this from the DataFrame. Requires time to be in string format.
        dfstartimestring = str(dfstartime)
        dfendtimestring = str(dfendtime)
        # Determine which algorithm to try based upon buy or sell
        if buyorsell == "buy":
            # Select the slice of the Dataframe, store in a separate dataframe. Have wrapped in a try statement while I deal with not enough data errors
            try:
                analysisdf = TokenDataFrame.loc[dfstartimestring:dfendtimestring]
                # Run through algorithm.
                outcome = algorithmone.algorithmonebuy(analysisdf, Tolerance=BuyTolerance)
                if outcome["Recommendation"] == "Buy":
                    buyrecommendations = buyrecommendations + 1
                    # Token will be purchased at the end price of DataFrame
                    purchaseprice = analysisdf.tail(1).Price.values[0]
                    # Update number of tokens purchased
                    numtokenspurchased = cashonhand / purchaseprice
                    # Cash on hand will be set to zero, so do this
                    cashonhand = 0
                    # Next action will be to sell these tokens, so change variable
                    buyorsell = "sell"
            except IndexError:
                result["IndexError"] = result["IndexError"] + 1
            except:
                print(f"Unexpected error in testalgorithm one function: {sys.exc_info()[0]}")
        elif buyorsell == "sell":
            # Select the slice of the Dataframe, store in a separate dataframe. Have wrapped in a try statement while I deal with not enough data errors
            try:
                analysisdf = TokenDataFrame.loc[dfstartimestring:dfendtimestring]
                # Run through algorithm.
                outcome = algorithmone.algorithmonesell(analysisdf, Tolerance=SellTolerance)
                if outcome["Recommendation"] == "Sell":
                    sellrecommendations = sellrecommendations + 1
                    # Token will be sold at the end price of DataFrame
                    sellprice = analysisdf.tail(1).Price.values[0]
                    # Calculate the cash generated from sale
                    cashonhand = numtokenspurchased * sellprice
                    # Set number of tokens back to zero
                    numtokenspurchased = 0
                    # Next action will be to buy so change variable
                    buyorsell = "buy"
            except IndexError:
                result["IndexError"] = result["IndexError"] + 1
            except:
                print(f"Unexpected error in testalgorithm one function:: {sys.exc_info()[0]}")
        else:
            # Some basic error handling
            print("Wrong outcome passed to buy or sell variable in function testalgorithmone")
        # Increment start time of algorithm
        dfstartime = dfstartime + numpy.timedelta64(1, 'm')
    # At the conclusion of the while loop, should have a number of results
    # Update number of buy and sell recommendations made
    result["BuyRecommendations"] = buyrecommendations
    result["SellRecommendations"] = sellrecommendations
    # If any units remaining, sell at final price to determine if algorithm was successful or not
    if numtokenspurchased != 0:
        # Get final sell price from TokenDataFrame
        finalsellprice = TokenDataFrame.tail(1).Price.values[0]
        # Sell and update cashonhand
        cashonhand = numtokenspurchased * finalsellprice
    # Update outcomes dictionary with cashonhand
    result["AlgorithmCash"] = cashonhand
    # Calculate total profit or loss amount
    profitorloss = cashonhand - InvestmentAmount
    result["ProfitLoss"] = profitorloss
    # Assess if algorithm provided success or failure
    if HODLOutcome > cashonhand:
        result["AlgorithmOutcome"] = "Failure"
    elif HODLOutcome < cashonhand:
        result["AlgorithmOutcome"] = "Success"
    elif HODLOutcome == cashonhand:
        result["AlgorithmOutcome"] = "NoBenefit"
    # Calculate the time taken on the algorithm
    end = timer()
    timetaken = end-start
    result["SecondsTaken"] = timetaken
    # Return outcome
    return result


# Fuction designed for use with MultiProcessor class
def testtoken(Token, Exchange, ProcessName):
    # Start timer on function
    start = timer()
    # Setup outcome dictionary for algorithm
    outcomedict = {
        "HoursAssessed": 576,
        "TimeTaken": 0,
        "Key": "testtoken",
        "DatabaseSearchTime": 0,
        "DateTime": str(datetime.datetime.now()),
        "Outcome": "",
        "Token": Token,
        "Exchange": Exchange,
        "ProcessName": ProcessName
    }
    # Get the token being assessed
    if Exchange == 'coinbase':
        query = {'base': Token}
        try:
            TokenDataFrame = genericdatamunging.getcoinbasepricedata(query)
            outcomedict["Outcome"] = "TokenSearched"
        except:
            print(f"Unexpected error in searching for data (testtoken function): {sys.exc_info()[0]}")
            outcomedict["Outcome"] = "SearchFailed"
    elif Exchange == 'binance':
        query = {"symbol": Token}
        try:
            TokenDataFrame = genericdatamunging.getlastbinancepricedata(query)
            outcomedict["Outcome"] = "TokenSearched"
        except:
            outcomedict["Outcome"] = "SearchFailed"
            print(f"Unexpected error in searching for data (testtoken function): {sys.exc_info()[0]}")
    else:
        outcomedict["Outcome"] = "SearchFailed"
        print(outcomedict)
        return outcomedict

    dbsearchtime = timer()
    timetaken = dbsearchtime - start
    outcomedict["DatabaseSearchTime"] = timetaken

    if outcomedict["Outcome"] == "TokenSearched":
        # Pass returned dataframe to be analysed
        result = testalgorithmone(TokenDataFrame=TokenDataFrame, InvestmentAmount=10000, SellTolerance=0.1, BuyTolerance=0.1)
        outcomedict["result"] = result
        # Insert result into mongodb
        mongodb.insertsingleintoalgorithmonewargame(result)
        # Update outcome
        outcomedict["Outcome"] = "TokenAnalysed"
    else:
        print("Token unable to be analysed as Token search failed")
    totaltime = timer()
    timetaken = totaltime - start
    outcomedict["TimeTaken"] = timetaken
    # Insert into mongodb
    mongodb.insertsingleintoalgorithmonewargame(outcomedict)
    return outcomedict
