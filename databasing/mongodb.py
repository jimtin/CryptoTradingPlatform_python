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

# Retrieve data from mongodb
def retrivesingleresult(Database, Collection):
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
def retrievesingleexchangeresult(exchange):
    outcome = retrivesingleresult("CryptoExchange", exchange)
    return outcome
