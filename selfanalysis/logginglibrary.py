import datetime
from databasing import mongodb

# Class for logging information for application
def logging(message, messagelevel):
    # Define collection based upon messagelevel
    if messagelevel == "info":
        coll = "info"
    elif messagelevel == "selfanalysis":
        coll = "selfanalysis"
    elif messagelevel == "warning":
        coll = "warning"
    elif messagelevel == "critical":
        coll = "critical"
    else:
        output = input("Wrong level indicated. Please input 'info', 'selfanalysis', 'warning' or 'critical'")
        logging(message, output)
    # Insert into MongoDb
    mongodb.insertsingledata("LoggingDatabase", coll, message)

# Wrapper to log generic function time events
def logfunctiontime(Function, TimeTaken):
    # Create the object to be inserted
    functionobject = {
        "Function": Function,
        "TimeTaken": TimeTaken,
        "DateTime": str(datetime.datetime.now())
    }
    logging(functionobject, "selfanalysis")

# Wrapper to log algorithm events
def logalgorithmselfanalysisevents(Algorithm, TimeTaken, NumberofTokens):
    # Create the Python Object to be inserted into the database
    algorithmobject = {
        "Algorithm": Algorithm,
        "TimeTaken": TimeTaken,
        "NumberofTokens": NumberofTokens,
        "DateTime": str(datetime.datetime.now())
    }
    logging(algorithmobject, "selfanalysis")
