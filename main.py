from ParallelProcessing import parallelprocessing
import pyfiglet
import multiprocessing
import datagathering
from Trading import AlgorithmImplementation
import multiprocessing


# Function to understand why I can't add stuff from a library
def startthread():
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)

# Main function for CryptoTrading platform
# set to start upon being called
if __name__ == "__main__":
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)
    # Set up a list of threads
    jobs = []
    # Setup Data gathering thread
    data = multiprocessing.Process(target=datagathering.getexchangedata, args=(True, ))
    data.start()
    jobs.append(data)
    # Now set up the Algorithm thread
    algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(0.5, True))
    jobs.append(algorithm)
    algorithm.start()


