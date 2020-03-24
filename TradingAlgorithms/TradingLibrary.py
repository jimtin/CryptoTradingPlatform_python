import splunk_as_a_database
from binance import binancetradingalgorithms
from binance import binancedatasearching
from coinbase import coinbasetradingalgorithm
from coinbase import coinbasedatasearching
import datetime
import json

### Library of trading algorithms and details for recording outcomes

# HypothesisOne: If a tokens price rises in two consecutive hours, then it will rise in the third hour also
# Further detail: User can input tolerances, default is 2%

def hypothesisone(BinanceTokens, CoinbaseTokens, SplunkSettingsFilepath, SplunkToken, Tolerance=2):
    # Load Splunk settings into function
    SplunkSettings = splunk_as_a_database.getsplunksettings(SplunkSettingsFilepath)
    # Iterate through Binance Tokens
    for token in BinanceTokens.symbol.items():
        # Convert Token name into a string
        symbol = str(token[1])
        Token = symbol
        # Get the data about the token
        tokendata = binancedatasearching.searchbinancedata(Token, "24h", SplunkSettingsFilepath, SplunkToken)
        # Analyse data to get the outcome
        outcome = binancetradingalgorithms.hypothesisone(tokendata, Tolerance)
        print(Token + ": " + outcome)
        # Construct a dictionary to store the result
        resultdict = {
            "DateTime": str(datetime.datetime.now()),
            "Exchange": "Binance",
            "Token": Token,
            "Recommendation": outcome,
            "TradingAlgorithm": "PercentRiseperTwoHours",
            "Tolerance": Tolerance
        }
        # Turn into JSON
        resultjson = json.dumps(resultdict)
        # Send result to Splunk
        splunk_as_a_database.splunkudpportsender(resultjson, SplunkIP=SplunkSettings["SplunkIP"],
                                                 SplunkPort=SplunkSettings["TradingDataPort"])
    # Iterate through Coinbase Tokens
    for base in CoinbaseTokens.base.items():
        # Convert Token name into a string
        basetoken = str(base[1])
        Token = basetoken
        # Get data about the token
        tokendata = coinbasedatasearching.searchcoinbasedata(Token, "24h", SplunkSettingsFilepath, SplunkToken)
        outcome = coinbasetradingalgorithm.hypothesisone(tokendata, Tolerance)
        # print(outcome)
        print(Token + ": " + outcome)
        # Construct a dictionary to store the result
        resultdict = {
            "DateTime": str(datetime.datetime.now()),
            "Exchange": "Coinbase",
            "Token": Token,
            "Recommendation": outcome,
            "TradingAlgorithm": "PercentRiseperTwoHours",
            "Tolerance": Tolerance
        }
        # Turn into JSON
        resultjson = json.dumps(resultdict)
        # Send result to Splunk
        # splunk_as_a_database.splunkudpportsender(resultjson, SplunkIP=SplunkSettings["SplunkIP"],
                                                 # SplunkPort=SplunkSettings["TradingDataPort"])




