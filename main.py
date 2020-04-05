import pyfiglet
import datagathering
from Trading import AlgorithmImplementation
import multiprocessing


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


