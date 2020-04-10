import pyfiglet
from datagathering import datagathering
from Trading import AlgorithmImplementation
import multiprocessing
from selfanalysis import dbanalysisclass
from selfanalysis import performanceanalysislibrary

# Function to remove worker process from jobs list
def removerworkerproc(ProcessName, jobs):
    # Find the index number in jobs list
    index = jobs.index(ProcessName)
    print(index)

# Main function for CryptoTrading platform
# set to start upon being called
if __name__ == "__main__":
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)

    # Set up variable names
    datagatheringname = "DataGatheringProcess"
    algorithmname = "AlgorithmProcess"
    tolerance = 0.5

    # Set up a list of processes
    jobs = []
    # First setup the self analysis process and confirm that mongodb is running

    # Setup Data gathering process
    data = multiprocessing.Process(target=datagathering.getexchangedata, args=(True,), name=datagatheringname)
    data.start()
    jobs.append(data)
    # Now set up the Algorithm process
    algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(tolerance, True), name=algorithmname)
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
        elif text == 'stop algorithms':
            print("Stopping algorithms")
            algorithm.terminate()
        elif text == 'start algorithms':
            print("Starting algorithms process")
            algorithm.start()
        elif text == 'change tolerance':
            # Get new tolerance
            tolerance = input("New tolerance? ")
            tolerance = float(tolerance)
            print(f'New Tolerance changed to: {tolerance}')
            # Stop algorithm process
            algorithm.terminate()
            # remove algorithm process from jobs list
            jobs.remove(algorithm)
            algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(tolerance, True),
                                                name=algorithmname)
            jobs.append(algorithm)
            algorithm.start()
        elif text == 'q':
            # Notify user that you are exiting the program
            print("Exiting program")
            # Send terminate command to all processes. Not pretty or graceful but will work on that later
            for proc in jobs:
                proc.terminate()
                runprogram = False
        else:
            print("Invalid text")


