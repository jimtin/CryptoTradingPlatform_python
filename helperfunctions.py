import splunk_as_a_database
import pandas

#############################################################################
# A series of helper functions for use with the cryptotrading platform
#############################################################################

# Function to construct initial splunk query
def constructexchangesplunksearch(exchange, FilePath, timeframe="24h"):
    # Ensure exchange is presented as a string
    exchange = str(exchange)
    # Ensure timeframe is presented as a string
    timeframe = str(timeframe)
    # The timeframe for splunk searches within searches can be found here: https://docs.splunk.com/Documentation/Splunk/8.0.2/Search/Specifytimemodifiersinyoursearch
    # For ease of use, will specify only 3 options for this search. 2 hours, 24 hours, 7 days
    # Using this information, construct the splunk search
    # Construct initial Splunk search
    splunksearch = "search index=* exchange=" + exchange
    # Now split based upon the input to timeframe
    if timeframe == "24h":
        splunksearch = splunksearch + " earliest=-24h latest=now"
    elif timeframe == "7d":
        splunksearch = splunksearch + " earliest=-7d latest=now"
    elif timeframe == "2h":
        splunksearch = splunksearch + " earliest=-2h latest=now"
    else:
        print("Incorrect value put in. Please use 2h, 24h or 7d")
        return "IncorrectValue"
    return splunksearch


# Search for values in a dictionary
def searchdict(list, searchdictval, searchterm):
    for k in list:
        if k[searchdictval] == searchterm:
            return True
    return False


# Function to convert the results from splunk into a pandas dataframe
# Assume: Input is a list, input is from coinbase
def getdataframe(data):
    # I can assume that all incoming data has the same DateTime field as put in there by this program
    # Therefore, index based upon time
    # First create a DataFrame
    df = pandas.DataFrame(data)
    # Now extract the DateTime strings and turn into DateTime objects
    datetime_series = pandas.to_datetime(df["DateTime"])
    # Now create this an index
    datetime_index = pandas.DatetimeIndex(datetime_series)
    # Create second dataframe with the index as a DateTime
    df2 = pandas.DataFrame(data, index=datetime_index)
    df2 = df2.drop(columns="DateTime")
    return df2




