import logging
import datetime

# Class to define coinbase data and how I want to work with it
class token:
    # Define the basics of a token - those attributes I don't want to change no matter what.
    def __init__(self, tokenname, tokenprice, currency, exchange):
        # Then name of a token
        self.tokenname = tokenname
        # The price of the token
        self.tokenprice = tokenprice
        # The currency the price is base off (i.e. USD)
        self.currency = currency
        # The exchange the token came from
        self.exchange = exchange

    # Function to capture when a token was retrieved from external source (i.e. queried from an exchange
    def getdateoftokenretrieval(self):
        now = datetime.datetime.now()
        return now