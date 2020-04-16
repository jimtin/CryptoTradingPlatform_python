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
def testcoinbasealgorithmone(Token, InvestmentAmount):
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
            # todo: turn this into a non silent error handle
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
    # Start timer on function
    start = timer()
    # Get a list of coinbase tokens
    coinbaselist = coinbasedatasearching.getuniquecoinbasetokens()
    for token in coinbaselist:
        print(f'Now testing {token}')
        query = {'base': token}
        # Get the token data
        TokenDataFrame = genericdatamunging.getcoinbasepricedata(query)
        result = testalgorithmone(TokenDataFrame=TokenDataFrame, InvestmentAmount=10000, SellTolerance=0.1, BuyTolerance=0.1)
        print(result)
    # Finish timer on function
    end = timer()
    # Calculate the time taken
    timetaken = end - start
    # Notify the user
    print(f'Time taken was {timetaken} seconds on testallcoinbasetokens')

def testbinancealgorithmone(Token, InvestmentAmount):
    # Start a timer on the function so it can be measured
    start = timer()
    # Get the entries for a single binance token
    query = {'symbol': Token}
    # Get data from the database
    TokenDataFrame = genericdatamunging.getlastbinancepricedata(query)
    # Get the start time of the data
    startime = TokenDataFrame.head(1).index.values[0]
    # Get the stop time of the data
    stoptime = TokenDataFrame.tail(1).index.values[0]
    # Define success
    # First, get the start price
    startprice = TokenDataFrame.head(1).Price.values[0]
    # Second, get the end price
    endprice = TokenDataFrame.tail(1).Price.values[0]
    # Calculate the delta
    change = endprice - startprice
    # Calculate the number of units which could have been purchased with the investment amount
    numunits = InvestmentAmount/startprice
    # Calculate success amount
    successamount = numunits * change
    print(f'Success criteria for {Token} is {successamount}')
    # Create a list to store outcomes while testing
    analysisresults = []
    # Create a maximum value for the iteration to come. This will make sure algorithm doesn't fail
    endtime = stoptime - numpy.timedelta64(5, 'h')
    # Move start time to a different variable so as not to mess up original data
    dfstarttime = startime
    # Iterate through dataframe using 1 minute intervals
    while dfstarttime < endtime:
        # Get the 5 hour window slice from the Dataframe
        dfendtime = dfstarttime + numpy.timedelta64(5, 'h')
        # Convert dfstart time and dfendtime into strings. This is required to get the slice from DataFrame
        dfstarttimestring = str(dfstarttime)
        dfendtimestring = str(dfendtime)
        # Get the Dataframe slice. Place in a try / except statement to enable error handling
        try:
            analysisdf = TokenDataFrame.loc[dfstarttimestring:dfendtimestring]
            # Run algorithmonebuy. Tolerance hardcoded in while data exploration occuring
            outcome = algorithmone.algorithmonebuy(analysisdf, Tolerance=0.1)
            # Create recommendation dictionary
            print(outcome)
            if outcome["Recommendation"] == "Buy":
                print((outcome["Recommendation"]))
            # Store result in list.
            analysisresults.append(outcome)
        except:
            # todo: turn this into a non silent error
            error = "Error"
        # Add one minute to dfstarttime
        dfstarttime = dfstarttime + numpy.timedelta64(1, 'm')

    # End the timer
    end = timer()
    # Calculate the time taken
    timetaken = end - start
    # Notify user how long this has taken
    print(f"Time taken on algorithm was {timetaken}")
    return analysisresults


# Get unique binance tokens and iterate through
def testallbinancetokens():
    # Start timer on function
    start = timer()
    # Get a list of unique binance tokens
    binancelist = binancedatasearching.getuniquebinancetokens()
    # Iterate through to get results
    for token in binancelist:
        print(f'Now testing {token}')
        query = {'symbol': token}
        # Get the token data
        TokenDataFrame = genericdatamunging.getlastbinancepricedata(query)
        result = testalgorithmone(TokenDataFrame=TokenDataFrame, InvestmentAmount=10000, SellTolerance=0.1,
                                  BuyTolerance=0.1)
        print(result)
    end = timer()
    # Calculate the time taken on function
    timetaken = end - start
    # Notify the user
    print(f'Time taken was {timetaken} seconds on testallbinancetokens')


# Create generic algorithm one test function. Assume TokenDataFrame has been passed through generic datamunging so data is consistent
def testalgorithmone(TokenDataFrame, InvestmentAmount, BuyTolerance, SellTolerance):
    # Start the timer on the function
    start = timer()
    # Create the results dictionary
    result = {
        "Token": "",
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
    }
    # Todo: implement multithreading on this
    # Get the Token name, store in dictionary
    tokenname = TokenDataFrame.tail(1).Token.values[0]
    result["Token"] = tokenname
    # Figure out what success would look like (HODL)
    startprice = TokenDataFrame.head(1).Price.values[0]
    endprice = TokenDataFrame.tail(1).Price.values[0]
    pricechange = endprice - startprice
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
            except:
                # todo: turn this into a non silent error handle
                error = "Error"
        elif buyorsell == "sell":
            # Select the slice of the Dataframe, store in a separate dataframe. Have wrapped in a try statement while I deal with not enough data errors
            try:
                analysisdf = TokenDataFrame.loc[dfstartimestring:dfendtimestring]
                # Run through algorithm.
                outcome = algorithmone.algorithmonesell(analysisdf, Tolerance=SellTolerance)
                if outcome["Recommendation"] == "Sell":
                    buyrecommendations = sellrecommendations + 1
                    # Token will be sold at the end price of DataFrame
                    sellprice = analysisdf.tail(1).Price.values[0]
                    # Calculate the cash generated from sale
                    cashonhand = numtokenspurchased * sellprice
                    # Set number of tokens back to zero
                    numtokenspurchased = 0
                    # Next action will be to buy so change variable
                    buyorsell = "buy"
            except:
                # todo: turn this into a non silent error handle
                error = "Error"
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

