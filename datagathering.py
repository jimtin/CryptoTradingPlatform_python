from binance import binanceAPIlibrary
from coinbase import coinbaselibrary


# function to get data from exchanges and put in MongoDB
def getexchangedata(Start=False):
    print("Starting data gathering")
    while Start==True:
        # Get data from binance
        binanceAPIlibrary.getpricechanges()
        # Instantiate the currently supported list of data from coinbase
        coinbaselist = ["BTC-USD", "ETH-USD", "XRP-USD", "BCH-USD", "BSV-USD", "LTC-USD", "EOS-USD", "XTZ-USD", "XLM-USD",
                        "LINK-USD", "DASH-USD", "ETC-USD", "ATOM-USD", "ZEC-USD", "BAT-USD", "ZRX-USD", "REP-USD",
                        "KNC-USD",
                        "DAI-USD"]
        # Get data from coinbase
        coinbaselibrary.getlistfromcoinbase(coinbaselist)
        # Update myself while troubleshooting
        print("Round complete, starting new round")


