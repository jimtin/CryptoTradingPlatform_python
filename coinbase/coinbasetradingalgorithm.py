import pandas


# Initial trading algorithm for coinbase
# First Hypothesis: If the average price per hour of a currency rises for two consecutive hours by more than a specified percentage (tolerance), the third hour will also rise
def hypothesisone(DataFrame, Tolerance):
    # First, take the DataFrame and split into hours
    DataFrame = DataFrame.groupby(DataFrame.index.hour).mean()
    # Check the length. If less than 4 hours, not enough data
    if len(DataFrame.index) < 5:
        outcome = "Not enough data"
        return outcome
    else:
        # Second, get the percentage change of token per hour
        # Note: I'm currently using a 24h search. The first row of pct_change will always return with NaN as it has one value.
        # This is slightly expensive for the Splunk search, but only marginally so have kept it
        HourChange = DataFrame.pct_change()
        # Test against the tolerance using a lambda function
        HourChange["MetTolerance"] = HourChange["amount"].apply(lambda x: "True" if x >= Tolerance else "False")
        # Now select final two hours
        TwoHours = HourChange.tail(2)
        # See if they have risen by the tolerance
        if TwoHours.take([0]).MetTolerance.item() == "True":
            if TwoHours.take([0]).MetTolerance.item() == "True":
                outcome = "Buy"
                return outcome
            else:
                outcome = "Partial Buy"
                return outcome
        else:
            outcome = "Do not buy"
            return outcome

