from binance import binanceAPIlibrary
from coinbase import coinbaselibrary
from timeit import default_timer as timer
from selfanalysis import logginglibrary
import time


# function to get data from exchanges and put in MongoDB
def getexchangedata(Start=False):
    while Start==True:
        # Time the function to see how long it takes to execute
        start = timer()
        # Get data from binance
        try:
            binanceAPIlibrary.getpricechanges()
        except:
            print("Binance datagathering error observed, continuing")
            time.sleep(10)
            # todo: add an exception for when there is no network, as this could go a bit futher

        try:
            # Instantiate the currently supported list of data from coinbase
            coinbaselist = ["BTC-USD", "ETH-USD", "XRP-USD", "BCH-USD", "BSV-USD", "LTC-USD", "EOS-USD", "XTZ-USD", "XLM-USD",
                            "LINK-USD", "DASH-USD", "ETC-USD", "ATOM-USD", "ZEC-USD", "BAT-USD", "ZRX-USD", "REP-USD",
                            "KNC-USD",
                            "DAI-USD"]
            # Get data from coinbase
            coinbaselibrary.getlistfromcoinbase(coinbaselist)
        except:
            print("Coinbase datagathering error observed")
            time.sleep(10)
            # todo: add an exception for when there is no network, as this could go a bit further

        # Get the end time of the timer
        end = timer()
        # Calculate time in seconds of execution
        executetime = end - start
        # Log the length of time it has taken
        logginglibrary.logfunctiontime("getexchangedata", executetime)


