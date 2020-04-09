import pyfiglet
import datagathering
from Trading import AlgorithmImplementation
import multiprocessing
from selfanalysis import dbanalysisclass
from selfanalysis import performanceanalysislibrary

# Main function for CryptoTrading platform
# set to start upon being called
if __name__ == "__main__":
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)

    # Set up the user input field
    manager = multiprocessing.Manager()
    go_flag = manager.Value('flag', True)

    # Set up a list of processes
    jobs = []
    # First setup the self analysis process and confirm that mongodb is running

    # Setup Data gathering process
    data = multiprocessing.Process(target=datagathering.getexchangedata, args=(True, ), name="DataGatheringProcess")
    data.start()
    jobs.append(data)
    # Now set up the Algorithm process
    algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(0.5, True), name="AlgorithmProcess")
    jobs.append(algorithm)
    algorithm.start()

    runprogram = True

    # Wait for user input
    while runprogram == True:
        text = input('Input command: ')
        if text == 'performance':
            # Setup a process to get the status
            performanceanalysislibrary.getperformanceoffunctions(24)
        elif text == 'status':
            # Query the jobs list to check on status
            for proc in jobs:
                print(f'Process Name: {proc.name}')
                print(f'Process Status: {proc.is_alive()}')
                print(f'Process PID: {proc.pid}')
        elif text == 'q':
            # Notify user that you are exiting the program
            print("Exiting program")
            # Send terminate command to all processes. Not pretty or graceful but will work on that later
            for proc in jobs:
                proc.terminate()
                runprogram = False




# Function to make sure database is up and running properly
def makesuredbisworking(Database):
    # Create the self analysis object
    analysisobject = dbanalysisclass.selfanalysis(Database)
    # Check the database is running, if not restart
    analysisobject.checkandrestartdatabase()


