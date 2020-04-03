import pyfiglet # For a bit of fun :)
from binance import binanceAPIlibrary
from coinbase import coinbaselibrary


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

main()


