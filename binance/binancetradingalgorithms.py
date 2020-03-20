from binance import binancedatasearching
import pandas
import matplotlib.pyplot as pyplot
from coinbase import coinbasedatasearching
import json

########################################################################################################################
# Library to explore trading hypothesis for binance
########################################################################################################################

# Trade Hypothesis 1: If price increases each hour over 2 hours, the next hour will see another price rise

# Function to explore Hypothesis 1
def hypothesisone(DataFrame, Tolerance):
    # First, take the DataFrame, split it into hours
    DataFrame = DataFrame.groupby(DataFrame.index.hour).mean()
    if len(DataFrame.index) < 5:
        outcome = "Not enough data"
        return outcome
    else:
        # Second, get the percentage change of token per hour
        # Note: I'm currently using a 24h search. The first row of pct_change will always return with NaN as it has one value.
        # This is slightly expensive for the Splunk search, but only marginally so have kept it
        HourChange = DataFrame.pct_change()
        # Test against the tolerance using a lambda function
        HourChange["MetTolerance"] = HourChange["lastPrice"].apply(lambda x: "True" if x >= Tolerance else "False")
        # Now select final two hours
        TwoHours = HourChange.tail(2)
        # See if they have risen by the tolerance
        if TwoHours.take([0]).MetTolerance.item() == "True":
            if TwoHours.take([0]).MetTolerance.item() == "True":
                outcome = "Buy"
                return outcome
            else:
                outcome = "PartialBuy"
                return outcome
        else:
            outcome = "NoBuy"
            return outcome



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