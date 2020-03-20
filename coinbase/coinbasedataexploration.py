from binance.binancetradingalgorithms import gettokenpriceovertime
from coinbase import coinbasedatasearching
import pandas
import matplotlib.pyplot as pyplot

######################################################################
# Library to explore coinbase data
#######################################################################

# Simple linegraph of coinbase data
def coinbaselinegraph(DataFrame, token):
    # Sort the DataFrame according to dates
    df = DataFrame.sort_values('DateTime', ascending=True)
    df["DateTime"] = pandas.to_datetime(df["DateTime"])
    print(df)
    # Take the DataFrame and set up the plot
    df.plot(kind="line", x="DateTime", y="amount", color="red", title=token)
    pyplot.show()


# Get simple coinbase analysis of single token
def simplecoinbaseplot(token, timeframe, FilePath):
    mungeddata = coinbasedatasearching.searchcoinbasedata(token, timeframe, FilePath)
    # Plot simple line graph
    coinbaselinegraph(mungeddata, token)


# Group dataframe data into hours
# Function assumes that DataFrame comes from the searchcoinbasedata function, which has already formatted objects
def groupcoinbasebyhour(DataFrame):
    # Group into hourly amounts
    DataFrame = DataFrame.groupby(DataFrame.index.hour).mean()
    return DataFrame




