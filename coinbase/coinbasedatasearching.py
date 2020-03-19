import helperfunctions
import splunk_as_a_database
import pandas

# Library for searching coinbase data from splunk


# Function to handle the searching
def searchcoinbasedata(token, timeframe, FilePath):
    # Confirm if the tokes provided are 1 or many (list)
    if isinstance(token, str):
        tokeninfo = searchsingletoken(token, timeframe, FilePath)
        return tokeninfo


# Function to search a single token from splunk
def searchsingletoken(token, timeframe, FilePath):
    # Construct the initial query
    basequery = helperfunctions.constructexchangesplunksearch("coinbase", FilePath, timeframe)
    # For coinbase, use base to get token symbol
    splunkquery = basequery + " base=" + token + " | table DateTime, amount, base"
    # The list search term will need to know how to search
    searchterm = "base"
    tokeninfo = splunk_as_a_database.querysplunk(splunkquery, FilePath)
    # Convert returned info into a dataframe
    tokeninfo = helperfunctions.getdataframe(tokeninfo)
    # Take dataframe and munge data into the objects required for further investigation
    tokeninfo = mungecoinbasedata(tokeninfo)
    # Returns a dataframe with data correctly munged
    return tokeninfo


# Munge coinbase data into a cool dataframe
def mungecoinbasedata(DataFrame):
    # Convert the amount to a float
    DataFrame["amount"] = pandas.to_numeric(DataFrame["amount"])
    # Convert the base to a string
    # DataFrame["base"] = DataFrame["base"].to_string()
    return DataFrame


# Function to get a list of tokens being searched and saved from Coinbase
def getlistofcoinbasetokens(timeframe, FilePath, sessionkey=""):
    # Construct the initial query
    basequery = helperfunctions.constructexchangesplunksearch("coinbase", FilePath, timeframe)
    splunkquery = basequery + " | dedup base | table base"
    tokenlist = splunk_as_a_database.querysplunk(splunkquery, FilePath, sessionkey)
    return tokenlist


