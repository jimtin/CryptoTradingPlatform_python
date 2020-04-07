import pyfiglet
import datagathering
from Trading import AlgorithmImplementation
import multiprocessing
from selfanalysis import selfanalysis


# Main function for CryptoTrading platform
# set to start upon being called
if __name__ == "__main__":
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)
    # Set up a list of processes
    jobs = []
    # First setup the self analysis process and confirm that mongodb is running

    # Setup Data gathering process
    data = multiprocessing.Process(target=datagathering.getexchangedata, args=(True, ))
    data.start()
    jobs.append(data)
    # Now set up the Algorithm process
    algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(0.5, True))
    jobs.append(algorithm)
    algorithm.start()


# Function to make sure database is up and running properly
def makesuredbisworking(Database):
    # Create the self analysis object
    analysisobject = selfanalysis.selfanalysis(Database)
    # Check the database is running, if not restart
    analysisobject.checkandrestartdatabase()