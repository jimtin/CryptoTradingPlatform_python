import datetime

# Algorithm Hypothesis: if the price of a token rises for two consecutive hours by a specified amount, it will rise in
# the following hour.
# User inputs tolerance. Default is 2%

# Function to take a Dataframe for a token and determine percentage rise for past four hours. If meets tolerance, buy is recommended.
def algorithmonebuy(TokenDataFrame, Tolerance=2):
    # Get the name of the token being analysed
    tokenname = TokenDataFrame.tail(1).Token.values[0]
    # Get the name of the exchange being analysed
    exchange = TokenDataFrame.tail(1).Exchange.values[0]
    # Group the DataFrame into hours
    TokenDataFrame = TokenDataFrame.groupby(TokenDataFrame.index.hour).mean()
    # Set up outcome variable
    resultdict = {
        "DateTime": str(datetime.datetime.now()),
        "Exchange": exchange,
        "Token": tokenname,
        "Recommendation": "",
        "TradingAlgorithm": "algorithmonebuy",
        "Tolerance": Tolerance
    }
    # Test the length of the DataFrame, make sure it is greater than 4, otherwise not enough data
    if len(TokenDataFrame.index) < 5:
        resultdict["Recommendation"] = "NotEnoughData"
        return resultdict
    else:
        # Get percentage change of token per hour
        HourChange = TokenDataFrame.pct_change()
        # Test against the tolerance using a lambda function
        HourChange["MetTolerance"] = HourChange["Price"].apply(lambda x: "True" if x >= Tolerance else "False")
        # Select final two hours
        TwoHours = HourChange.tail(2)
        # See if price rise has risen by tolerance
        # See if they have risen by the tolerance
        if TwoHours.take([0]).MetTolerance.item() == "True":
            if TwoHours.take([0]).MetTolerance.item() == "True":
                resultdict["Recommendation"] = "Buy"
            else:
                resultdict["Recommendation"] = "PartialBuy"
        else:
            resultdict["Recommendation"] = "NoBuy"
        return resultdict


# Define when to sell a Token
# Central hypothesis: If a token falls by specified tolerance for two hours, it will fall the third. Therefore you should sell.
def algorithmonesell(TokenDataFrame, Tolerance=2):
    # Get the name of the token being analysed
    tokenname = TokenDataFrame.tail(1).Token.values[0]
    # Get the name of the exchange being analysed
    exchange = TokenDataFrame.tail(1).Exchange.values[0]
    # Group the DataFrame into hours
    TokenDataFrame = TokenDataFrame.groupby(TokenDataFrame.index.hour).mean()
    # Set up outcome variable
    resultdict = {
        "DateTime": str(datetime.datetime.now()),
        "Exchange": exchange,
        "Token": tokenname,
        "Recommendation": "",
        "TradingAlgorithm": "algorithmonesell",
        "Tolerance": Tolerance
    }
    # Test the length of the DataFrame, make sure it is greater than 4, otherwise not enough data
    if len(TokenDataFrame.index) < 5:
        resultdict["Recommendation"] = "NotEnoughData"
        return resultdict
    else:
        # Get percentage change of token per hour
        HourChange = TokenDataFrame.pct_change()
        # Test against the tolerance using a lambda function
        HourChange["MetTolerance"] = HourChange["Price"].apply(lambda x: "True" if x <= Tolerance else "False")
        # Select final two hours
        TwoHours = HourChange.tail(2)
        # See if price rise has fallen by tolerance
        # See if they have fallen by the tolerance
        if TwoHours.take([0]).MetTolerance.item() == "True":
            if TwoHours.take([0]).MetTolerance.item() == "True":
                resultdict["Recommendation"] = "Sell"
            else:
                resultdict["Recommendation"] = "PartialSell"
        else:
            resultdict["Recommendation"] = "NoSell"
        return resultdict
