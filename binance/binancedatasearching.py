import helperfunctions
import splunk_as_a_database
import pandas

# Library for searching binance data

# Function to handle the searching binance data from splunk
def searchbinancedata(token, timeframe, FilePath, SplunkToken):
    # Confirm if the tokens provided are 1 or many (list)
    # If single, could be a string, or a list with 1 element
    if isinstance(token, str):
        tokeninfo = searchsingletoken(token, timeframe, FilePath, SplunkToken)
        return tokeninfo


# Function for searching a single token
def searchsingletoken(token, timeframe, FilePath, SplunkToken):
    # Construct the initial query
    basequery = helperfunctions.constructexchangesplunksearch("binance", FilePath, timeframe)
    # For binance, use symbol to get token symbol
    splunkquery = basequery + " symbol=" + token + " | table DateTime, lastPrice"
    # The list search team will need to know how to search
    searchterm = "symbol"
    tokeninfo = splunk_as_a_database.querysplunk(splunkquery, FilePath, SplunkToken)
    # Convert returned info into a dataframe
    tokeninfo = helperfunctions.getdataframe(tokeninfo)
    # Take dataframe and munge data into the objects required for further investigation
    tokeninfo = mungebinancedata(tokeninfo)
    return tokeninfo


# Function to munge binance data into a reasonable dataframe
def mungebinancedata(DataFrame):
    # Convert lastPrice to a float
    DataFrame["lastPrice"] = pandas.to_numeric(DataFrame["lastPrice"])
    return DataFrame


# Function to get a list of tokens being searched and saved from Binance
def getlistofbinancetokens(timeframe, FilePath, sessionkey=""):
    basequery = helperfunctions.constructexchangesplunksearch("binance", FilePath, timeframe)
    splunkquery = basequery + " | dedup symbol | table symbol"
    tokenlist = splunk_as_a_database.querysplunk(splunkquery, FilePath, sessionkey)
    return tokenlist
