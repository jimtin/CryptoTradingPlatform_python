import platform
import os
from pymongo import MongoClient
import subprocess

# Database class
class Database:
    def __init__(self, Database):
        self.dbname = Database
        client = MongoClient()
        db = client[self.dbname]
        self.dbconnection = db

# Class to run self analysis on CryptoTrading platform
class dbanalysis(Database):
    def __init__(self, Database):
        super().__init__(Database)
        # Get the platform program is running on
        self.Platform = platform.system()
        # Set the name of the exchange database being used
        self.Database = Database
        if self.Platform == 'Linux':
            # Check the status of the database service
            proc = subprocess.run(["service", "mongod", "status"], stdout=subprocess.PIPE, shell=False)
            self.DatabaseStatus = proc.returncode
            # If status not 0, means there is an issue and should be addressed. If 0, means it is running
            if self.DatabaseStatus == 0:
                # If all is up and running, get stats about the database
                # Set up MongoClient
                client = MongoClient()
                db = client[self.Database]
                stats = db.command("dbstats")
                self.DatabaseSize = stats["dataSize"] / (1024 * 1024 * 1024)
            else:
                print(f"Database service mongod is not working. Current status is {self.DatabaseStatus}")
        else:
            print("Platform is not Linux, this functionality is not available")

    # Method to update database status
    def checkdatabasestatus(self):
        # Create the command string
        command = "service " + self.Database + " status"
        print(command)
        outcome = os.system(command)
        print(f"outcome = {outcome}")
        # Update status
        self.DatabaseStatus = outcome
        return outcome

    # Method to start database
    def startdatabase(self):
        # Create the start string
        command = "service " + self.Database + " start"
        print(command)
        # Run command
        os.system(command)
        # Check it is now running and update status accordingly
        dbstatus = self.checkdatabasestatus()
        if dbstatus != 0:
            print("database did not start. Exit program and fix")
        else:
            print("Database restarted")

    # Method to restart database
    def checkandrestartdatabase(self):
        # Check if database is running
        dbstatus = self.checkdatabasestatus()
        if dbstatus != 0:
            print("Database is not running properly, restarting")
            self.startdatabase()
        else:
            print("Database is working")

    # Method to update database size
    def updatedbsize(self):
        try:
            client = MongoClient()
            db = client[self.Database]
            stats = db.command("dbstats")
            self.DatabaseSize = stats["dataSize"] / (1024 * 1024 * 1024)
        except:
            print("Error updating db size")

