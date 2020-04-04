from ParallelProcessing import parallelprocessing
import pyfiglet
import multiprocessing
import datagathering
from Trading import AlgorithmImplementation
from threading import Thread


# Function to understand why I can't add stuff from a library
def analysealgorithms(Toleranace):
    print(f"Tolerance is: {Toleranace}")
    AlgorithmImplementation.implementalgorithmone(Toleranace)

# Main function for CryptoTrading platform
# set to start upon being called
if __name__ == "__main__":
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)

    # Set up a list of threads
    threads = []
    # Trial threads
    test = Thread(target=analysealgorithms, args=(0.5,))
    test.start()
    threads.append(test)
    test.join()
    # Setup Data gathering thread
    data = Thread(target=datagathering.getexchangedata, args=(True, ))
    # data.start()
    threads.append(data)
    data.join()
    # Now set up the Algorithm thread
    algorithm = Thread(target=AlgorithmImplementation.implementalgorithmone, args=(0.5, ))
    # algorithm.start()
    threads.append(algorithm)
    algorithm.join()


def start():
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)

    # Set up a list of threads
    threads = []
    # Setup Data gathering thread
    data = Thread(target=datagathering.getexchangedata(), args=[True])
    data.start()
    threads.append(data)
    # Now set up the Algorithm thread
    algorithm = Thread(target=AlgorithmImplementation.implementalgorithmone(), args=[0.5, True])
    algorithm.start()
    threads.append(algorithm)


