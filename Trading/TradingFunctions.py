from databasing import mongodb
import datetime

# Library of functions to call depending on outcomes of AlgorithmImplementation
def purchasetoken(Token, Exchange):
    print(f'Purchase {Token} from {Exchange}')


# Function to get a list of buy recommendations from past period time
def getbuyrecommendationstimerange(StartTime, EndTime):
    # Turn the datetime objects into strings
    StartTime = str(StartTime)
    EndTime = str(EndTime)
    # Set up the query
    query = {'Recommendation': 'Buy', 'DateTime': {'$gte': StartTime, '$lte': EndTime}}
    timedata = mongodb.getquerydatafromcollection("TradingDatabase", "RawRecommendations", query)
    return timedata


# Function to get the lastest buy recommendations from past period of time
def getlatestbuyrecommendations(TimeFrame):
    # Get the latest time
    EndTime = datetime.datetime.now()
    StartTime = datetime.datetime.now() - datetime.timedelta(hours=TimeFrame)
    timedata = getbuyrecommendationstimerange(StartTime, EndTime)
    return timedata
