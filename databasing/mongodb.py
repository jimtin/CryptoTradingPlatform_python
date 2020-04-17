from pymongo import MongoClient

# Quick and dirty library to start capturing market data while I sort out OOP

# Function to insert returned values into mongo database one at a time
def insertsingledata(Database, collection, Data):
    # Make sure database is a string
    Database = str(Database)
    # Create connection to Mongo #todo: this will need to be authenticated in the future
    mongoclient = MongoClient()
    # Create a connection to the Database
    database = mongoclient[Database]
    # Create a connection to the collection
    collection = database[collection]
    dataupdate = collection.insert_one(Data)
    return dataupdate

# Function to insert returned values into mongo database many at a time
def insertmanydata(Database, collection, Data):
    # Make sure database is a string
    Database = str(Database)
    # Create connection to Mongo #todo: this will need to be authenticated in the future
    mongoclient = MongoClient()
    # Create a connection to the Database
    database = mongoclient[Database]
    # Create a connection to the collection
    collection = database[collection]
    dataupdate = collection.insert_many(Data)
    return dataupdate

# Wrapper for inserting into the Crytoexchange database
def insertsingleintocrypto(exchange, Data):
    cryptoinsert = insertsingledata("CryptoExchange", exchange, Data)
    return cryptoinsert

# Wrapper for inserting many into the Cryptoexchange database
def insertmanyintocrypto(exchange, Data):
    cryptoinsert = insertmanydata("CryptoExchange", exchange, Data)
    return cryptoinsert

# Wrapper for inserting into the TradingRecommendations database
def insertsingleintotradingrecommendations(Data):
    recommendation = insertsingledata("TradingDatabase", "RawRecommendations", Data)
    return recommendation

# Wrapper for inserting into the AlgorithmOne wargaming function
def insertsingleintoalgorithmonewargame(Data):
    result = insertsingledata("AlgorithmOneWargaming", "TestingData", Data)
    return result

# Retrieve single row of data from mongodb
def getsingleresult(Database, Collection):
    # Make sure Database is a string
    Database = str(Database)
    # Create the client
    mongoclient = MongoClient()
    # Connect to Database
    database = mongoclient[Database]
    # Create collection
    collection = database[Collection]
    # do search
    result = collection.find_one()
    return result

# Wrapper for retrieving a single result from Cryptoexchange database and exchange
def getsingleexchangeresult(exchange):
    outcome = getsingleresult("CryptoExchange", exchange)
    return outcome

# Retrieve multiple rows of data from mongodb
def getalldatafromcollection(Database, Collection):
    # Make sure Database is a string
    Database = str(Database)
    # Create the client
    mongoclient = MongoClient()
    # Connect to Database
    database = mongoclient[Database]
    # Create a collection
    collection = database[Collection]
    # Get search
    result = collection.find()
    # Turn result into a list
    outcome = list(result)
    return outcome

# Retrieve all data from a Cryptoexchange collection
def getalldatafromexchange(exchange):
    # Get data from collection
    outcome = getalldatafromcollection("CryptoExchange", exchange)
    return outcome

# Retrieve data from a query
def getquerydatafromcollection(Database, Collection, Query):
    # Make sure Database is a string
    Database = str(Database)
    # Create the client
    mongoclient = MongoClient()
    # Connect to Database
    database = mongoclient[Database]
    # Create a collection
    collection = database[Collection]
    # Insert query
    result = collection.find(Query)
    # Turn result into a list
    outcome = list(result)
    # Return result to user
    return outcome

# Retrieve query data from binance
def getbinancequerydata(Query):
    # Get data from collection = binance
    outcome = getquerydatafromcollection("CryptoExchange", "binance", Query)
    return outcome

# Retrieve query data from coinbase
def getcoinbasequerydata(Query):
    outcome = getquerydatafromcollection("CryptoExchange", "coinbase", Query)
    return outcome

# Get a list of unique values in binance
def getuniquebinancetokens():
    # Create the client
    mongoclient = MongoClient()
    # Connect to Database
    database = mongoclient["CryptoExchange"]
    # Get collection
    collection = database["binance"]
    # Get unique values
    outcome = collection.distinct("symbol")
    return outcome

# Get a list of unique values in coinbase
def getuniquecoinbasetokens():
    # Create the client
    mongoclient = MongoClient()
    # Connect to Database
    database = mongoclient["CryptoExchange"]
    # Get collection
    collection = database["coinbase"]
    # Get unique values
    outcome = collection.distinct("base")
    return outcome

# Function to get result from AlgorithmOneWargaming database
def getsingleresultfromAlgorithmOneWargamingdatabase():
    # Create the client
    mongoclient = MongoClient()
    # Connect to the database
    database = mongoclient["AlgorithmOneWargaming"]
    # Connect to the collection
    collection = database["TestingData"]
    # Get the value
    outcome = collection.find_one()
    return outcome

# Function to get the latest result from AlgorithmOneWargaming for specified key
def getlatestresultfromAlgorithOneWargamingwithKey(Key):
    # Set up the query
    query = {'Key': Key}
    # Set up the client, database and collection
    mongoclient = MongoClient()
    collection = mongoclient["AlgorithmOneWargaming"]["TestingData"]
    outcome = collection.find(query).sort([("DateTime", -1)]).limit(1)
    outcome = list(outcome)
    return outcome


