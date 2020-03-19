from binance import binancedatasearching
import pandas
import matplotlib.pyplot as pyplot
from coinbase import coinbasedatasearching
import json


# Trade Hypothesis 1: If price increases each hour over 2 hours, the next hour will see another price rise
# Trade Hypothesis 2: If price stops increasing hour over hour, I should sell as it will fall soon
# Considerations: Optimising this algorithm will take time, as I will have limited resources to trade ALL rising stocks
# Benchmark against: BTC, ETH, EOS and BNB


# Function to get the average price over time of a token
def gettokenpriceovertime(exchange, token, timeframe, FilePath):

    # Search splunk to get a list of unique tokens for that exchange
    # Each exchange deals with things a little differently so will need to construct searches based on the exchange
    # Have already validated the exchange in the constructexchangesplunksearch function, so proceed on assumption it is valid
    # todo: expand this to be able to search an array / list of values
    if exchange == "binance":
        binancedatasearching.searchbinancedata(token, timeframe, FilePath)

    elif exchange == "coinbase":
        exchangedata = coinbasedatasearching.searchcoinbasedata(token, timeframe, FilePath)
        print(exchangedata)
    else:
        return False


# Function to get binance keys from the BinanceFilePath
def getbinancekeys(filepath):
    # Open the Binance Keys filepath
    f = open(filepath)
    # Format of the data will be json, so convert
    keydatajson = f.read()
    keydata = json.loads(keydatajson)
    # Create a dict with the keys
    Keys = keydata['binance']
    return Keys



