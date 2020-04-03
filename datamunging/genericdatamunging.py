from databasing import mongodb
import pandas
from timeit import default_timer as timer

# Library to convert data from various exchanges into a single coherent datatype. Output should always be a dataframe

# Get coinbase dataframe and munge into a consistent set of fields
def getlastcoinbasepricedata(Query):
    result = mongodb.getcoinbasequerydata(Query)
    df = pandas.DataFrame(result)
    # Convert column 'base' into a string, then rename to token
    df['base'] = df['base'].astype(str)
    df.rename(columns={'base': 'Token'}, inplace=True)
    # Convert column 'currency' into a string
    df['currency'] = df['currency'].astype(str)
    # Convert column 'amount' into a float, then change to price
    df['amount'] = df['amount'].astype(float)
    df.rename(columns={'amount': 'Price'}, inplace=True)
    # Convert column Exchange into string
    df['Exchange'] = df['Exchange'].astype(str)
    # Convert Column DateTimeGathered into DateTime object
    df['DateTimeGathered'] = pandas.to_datetime(df['DateTimeGathered'])
    # Now drop any rows with NaN or NaT
    df = df.dropna()
    # Create the index based upon DateTime object
    df.set_index('DateTimeGathered', inplace=True, drop=True)
    # Drop residual _id column
    df = df.drop('_id', axis=1)
    return df

# Get binance dataframe and munge into a consistent set of fields
def getlastbinancepricedata(Query):
    start = timer()
    result = mongodb.getbinancequerydata(Query)
    # Convert result into dataframe
    df = pandas.DataFrame(result)
    # Convert column 'symbol' into string, then rename to token
    df['symbol'] = df['symbol'].astype(str)
    df.rename(columns={'symbol': 'Token'}, inplace=True)
    # Convert column 'exchange' into string
    df['Exchange'] = df['Exchange'].astype(str)
    # Convert column lastPrice into float, then rename Price
    df['lastPrice'] = df['lastPrice'].astype(float)
    df.rename(columns={'lastPrice':'Price'}, inplace=True)
    # Convert column 'DateTimeGathered into DateTime object
    df['DateTimeGathered'] = pandas.to_datetime(df['DateTimeGathered'])
    # Now drop any rows with NaN or NaT
    df = df.dropna()
    # Drop ID column as no longer needed
    df = df.drop('_id', axis=1)
    # Create the index based upon DateTime object
    df.set_index('DateTimeGathered', inplace=True, drop=True)
    # Drop all the other rows. This may seem very manual, but it will allow future fields to be easily added back in
    #df = df.drop('priceChange', axis=1)
    #df = df.drop('priceChangePercent', axis=1)
    #df = df.drop('weightedAvgPrice', axis=1)
    #df = df.drop('prevClosePrice', axis=1)
    #df = df.drop('lastQty', axis=1)
    #df = df.drop('bidPrice', axis=1)
    #df = df.drop('bidQty', axis=1)
    #df = df.drop('askPrice', axis=1)
    #df = df.drop('askQty', axis=1)
    #df = df.drop('openPrice', axis=1)
    #df = df.drop('highPrice', axis=1)
    #df = df.drop('lowPrice', axis=1)
    #df = df.drop('volume', axis=1)
    #df = df.drop('quoteVolume', axis=1)
    #df = df.drop('openTime', axis=1)
    #df = df.drop('closeTime', axis=1)
    #df = df.drop('firstId', axis=1)
    #df = df.drop('lastId', axis=1)
    #df = df.drop('count', axis=1)

    end = timer()
    totaltime = end-start
    # print(totaltime)
    return df


