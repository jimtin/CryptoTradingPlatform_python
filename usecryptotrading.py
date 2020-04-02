from pathlib import Path
import pyfiglet # For a bit of fun :)
import json
from binance import binanceAPIlibrary
from time import sleep
import datetime
from coinbase import coinbaselibrary
from databasing import mongodb
import pandas


# Declare the Global Variables needed
Exchanges = pandas.DataFrame()
CoinbaseTokens = pandas.DataFrame()
BinanceTokens = pandas.DataFrame()
SplunkSettings = ""
BinanceFilepath = ""


# Get file path for keys
def main():
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Library")
    print(welcome_banner)

    while 1:
    # Get data from exchanges
        print("Getting binance prices")
        binanceAPIlibrary.getpricechanges()

        print("Getting coinbase spot prices")
        coinbaselist = ["BTC-USD", "ETH-USD", "XRP-USD", "BCH-USD", "BSV-USD", "LTC-USD", "EOS-USD", "XTZ-USD", "XLM-USD",
                        "LINK-USD", "DASH-USD", "ETC-USD", "ATOM-USD", "ZEC-USD", "BAT-USD", "ZRX-USD", "REP-USD",
                        "KNC-USD",
                        "DAI-USD"]
        coinbasespotprices = coinbaselibrary.getlistfromcoinbase(coinbaselist)


