from coinbase import coinbasedatasearching
import pandas
import datetime
import logging

# Algorithm Hypothesis: if the price of a token rises for two consecutive hours by a specified amount, it will rise in
# the following hour.
# User inputs tolerance. Default is 2%

# Function to take a Dataframe for a token and determine percentage rise for past four hours
def algorithmone(TokenDataFrame, Tolerance=2):
    # Set up the logging for this algorithm
    logging.basicConfig(format='%(asctime)s - %(process)d - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO, filename='app.log', filemode='a')
    # Get the name of the token being analysed
    tokenname = TokenDataFrame.tail(1).Token.values[0]
    # Get the name of the exchange being analysed
    exchange = TokenDataFrame.tail(1).Exchange.values[0]
    # Group the DataFrame into hours
    TokenDataFrame = TokenDataFrame.groupby(TokenDataFrame.index.hour).mean()
    # Test the length of the DataFrame, make sure it is greater than 4, otherwise not enough data
    if len(TokenDataFrame.index) < 5:
        logging.info(f'{tokenname} did not have enough results')
        outcome = "NotEnoughData"
        return outcome
    else:
        logging.info(f'{tokenname} getting analyzed, tolerance={Tolerance}')
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
                outcome = "Buy"
            else:
                outcome = "PartialBuy"
        else:
            outcome = "NoBuy"

        # Define the dictionary which will be returned by algorithm
        resultdict = {
            "DateTime": str(datetime.datetime.now()),
            "Exchange": exchange,
            "Token": tokenname,
            "Recommendation": outcome,
            "TradingAlgorithm": "algorithmone",
            "Tolerance": Tolerance
        }
        return resultdict

