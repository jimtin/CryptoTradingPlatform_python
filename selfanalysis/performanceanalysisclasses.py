from selfanalysis import dbanalysisclass
from databasing import mongodb
import datetime
import pandas

# Class to analyse the performance of application
class Performance:
    def __init__(self):
        # Confirm that self analysis database is up and running
        performancedb = dbanalysisclass.dbanalysis("LoggingDatabase")
        self.status = performancedb.DatabaseStatus
        self.database = "LoggingDatabase"

    # Method to get database name and return as a string
    def getdatabasename(self):
        name = self.database
        return name


class FunctionTimes(Performance):
    def __init__(self, function):
        # Initialise the super class
        super().__init__()
        self.function = function
        # Get the collection for timing
        self.dbcollection = "selfanalysis"

    # Method to get average execute time for a function
    def getaveragetime(self, TimeFrame):
        # Get data from database for timespan
        # Take TimeFrame and get the period of time this represents
        time = str(datetime.datetime.now() - datetime.timedelta(hours=TimeFrame))
        # Construct the query to send to MongoDb
        Query = {'Function': self.function, 'DateTime': {'$gt': time}}
        # Search database for the query
        database = self.database
        timedata = mongodb.getquerydatafromcollection(self.database, self.dbcollection, Query)
        # Turn into a DataFrame
        df = pandas.DataFrame(timedata)
        # Convert DateTime string into DateTime objects ready for indexing
        df['DateTime'] = pandas.to_datetime(df['DateTime'])
        # Drop any rows with NaN or NaT
        df = df.dropna()
        # Set index as DateTime object to give time sequenced data
        df.set_index('DateTime', inplace=True, drop=True)
        # Drop original ID column as no longer needed
        df = df.drop('_id', axis=1)
        # Convert TimeTaken column into a float
        df["TimeTaken"] = df["TimeTaken"].astype(float)
        # Now calculate mean
        meantime = df["TimeTaken"].mean()
        return meantime
