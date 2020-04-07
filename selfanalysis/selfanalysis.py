import platform
import os

# Class to run self analysis on CryptoTrading platform
class selfanalysis:
    def __init__(self, database):
        self.Platform = platform.system()
        self.Database = database
        if self.Platform == 'Linux':
            self.DatabaseStatus = os.system('service mongod status')
            # If status not 0, means there is an issue and should be addressed. If 0, means it is running
            if self.DatabaseStatus == 0:
                print("Database service mongod is running")
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



