from binance import binancedatasearching
import pandas

###############################################
### Library to explore binance data
###############################################

# Function to group binance dataframe objects into hours. Assumes data presented already munged.
def groupbinancebyhour(DataFrame):
    # Group into hourly amounts
    DataFrame = DataFrame.groupby(DataFrame.index.hour).mean()
    return DataFrame