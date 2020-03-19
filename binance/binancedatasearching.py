import helperfunctions
import splunk_as_a_database
import pandas

# Library for searching binance data

# Function to handle the searching binance data from splunk
def searchbinancedata(token, timeframe, FilePath):
    # Confirm if the tokens provided are 1 or many (list)
    # If single, could be a string, or a list with 1 element
    if isinstance(token, str):
        print("Single token provided, continuing")
        # todo: confirm tokens
        tokeninfo = searchsingletoken(token, timeframe, FilePath)
        return tokeninfo


# Function for searching a single token
def searchsingletoken(token, timeframe, FilePath):
    # Construct the initial query
    basequery = helperfunctions.constructexchangesplunksearch("binance", FilePath, timeframe)
    # For binance, use symbol to get token symbol
    # Confirm that token exists
    splunkquery = basequery + " | dedup symbol | table symbol"
    # The list search term will need to know how to search
    searchterm = "symbol"
    splunkquery = basequery + " symbol=" + token + " | table askPrice, bidPrice, DateTime, openPrice, priceChange, priceChangePercent"
    tokeninfo = splunk_as_a_database.querysplunk(splunkquery, FilePath)
    return tokeninfo


# Function to get a list of tokens being searched and saved from Binance
def getlistofbinancetokens(timeframe, FilePath, sessionkey=""):
    basequery = helperfunctions.constructexchangesplunksearch("binance", FilePath, timeframe)
    splunkquery = basequery + " | dedup symbol | table symbol"
    tokenlist = splunk_as_a_database.querysplunk(splunkquery, FilePath, sessionkey)
    return tokenlist

# todo: Munge binance data