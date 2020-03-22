from pymongo import MongoClient
import logging


# Class which describes / implements pymongo
class db:
    logging.basicConfig(filename="app.log", filemode="a", format='%(asctime)s %(name)s - %(levelname)s - %(message)s',level="INFO", datefmt='%d-%b-%y %H:%M:%S')
    def __init__(self, dbname):
        # Initialize the MongoClient
        self.client = MongoClient()
        # Using the Client, check if dbexists
        databaselist = self.client.list_database_names()
        if dbname in databaselist:
            logging.info(f"{dbname}already exists, continuing")
            self.database = self.client[dbname]
        else:
            logging.info(f"{dbname} does not exist, creating")
            self.database = self.client[dbname]

    # Get a list of databases from the connection
    def getlistofdatabases(self):
        databases = self.client.list_database_names()
        return databases

