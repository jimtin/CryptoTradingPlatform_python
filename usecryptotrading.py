from pathlib import Path
import pyfiglet # For a bit of fun :)
import json
from binance import binanceAPIlibrary
import splunk_as_a_database
from time import sleep
import datetime
from coinbase import coinbaselibrary
from coinbase import coinbasedatasearching
from binance import binancedatasearching
from coinbase import coinbasetradingalgorithm
from binance import binancetradingalgorithms
from TradingAlgorithms import TradingLibrary
from databasing import mongodb
import pandas


# Declare the Global Variables needed
Exchanges = pandas.DataFrame()
CoinbaseTokens = pandas.DataFrame()
BinanceTokens = pandas.DataFrame()
SplunkSettings = ""
BinanceFilepath = ""


# Get file path for keys
def main(BinanceFilepath=""):
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Library")
    print(welcome_banner)

    # Get data from exchanges
    print("Getting binance prices")
    binanceAPIlibrary.getpricechanges()

    print("Getting coinbase spot prices")
    coinbaselist = ["BTC-USD", "ETH-USD", "XRP-USD", "BCH-USD", "BSV-USD", "LTC-USD", "EOS-USD", "XTZ-USD", "XLM-USD",
                    "LINK-USD", "DASH-USD", "ETC-USD", "ATOM-USD", "ZEC-USD", "BAT-USD", "ZRX-USD", "REP-USD",
                    "KNC-USD",
                    "DAI-USD"]
    coinbasespotprices = coinbaselibrary.getlistfromcoinbase(coinbaselist)
    print(coinbasespotprices)
    insertdata = mongodb.insertmanyintocrypto("coinbase", coinbasespotprices)
    print(insertdata)

    # Setup the filepaths for getting settings
    # First: Get Binance keys
    if BinanceFilepath == "":
        print("No value supplied for Binance keys, please input values below")
        BinanceFilepath = input("Put Binance Settings filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    # Else statement just to ensure everything is captured
    else:
        BinanceFilepath = BinanceFilepath
    # Now turn into a Path variable using Path library. This allows it to be platform agnostic
    # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
    BinanceKeysFilePath = Path(BinanceFilepath)

    # Load the settings from the file into memory
    # binancekeys = binancetradingalgorithms.getbinancekeys(BinanceKeysFilePath)
    print("Binance Keys Loaded")

    # Load options from each exchange being saved to speed up future searching
    # Now get coinbase options, save to global variable
    #print("Loading Coinbase exchange tokens available")
    #coinbasetokens = coinbasedatasearching.getlistofcoinbasetokens("24h", SplunkSettings)
    #global CoinbaseTokens
    #CoinbaseTokens = pandas.DataFrame(coinbasetokens)
    # Advise user of the options available
    #print("Available Coinbase tokens:")
    #print(CoinbaseTokens)

    # Now get binance token list
    #print("Loading available Binance tokens:")
    #binancetokens = binancedatasearching.getlistofbinancetokens("24h", SplunkSettings, sessionkey)
    #global BinanceTokens
    #BinanceTokens = pandas.DataFrame(binancetokens)
    # Advise user of options available
    #print("Available Binance tokens:")
    #print(BinanceTokens)

    #while 1:
        # Search through available Binance tokens
    #    TradingLibrary.hypothesisone(BinanceTokens, CoinbaseTokens, SplunkSettingsFilepath, sessionkey, 2)


# Function to select which exchange and token to search
def tokenselection(token):
    # Declare the global variables being used
    global CoinbaseTokens
    global BinanceTokens
    # Setup a list of exchanges available in
    exchangesavailable = []
    # Check if element exists in Coinbase
    if token in CoinbaseTokens.values:
        exchangesavailable.append("coinbase")
    # Check if element exists in Binance
    if token in BinanceTokens.values:
        exchangesavailable.append("binance")
    return exchangesavailable

