import multiprocessing
import pyfiglet
import datagathering
from Trading import AlgorithmImplementation

# Main function for CryptoTrading platform
# set to start upon being called
if __name__ == "__main__":
    # Fun little welcome to CryptoTradingPlatform
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Platform")
    print(welcome_banner)
    # Define IPC manager
    manager = multiprocessing.Manager()

    # Define the queue for tasks and any required computation results
    tasks = manager.Queue()
    results = manager.Queue()

    # Get the number of processors available
    numcpu = multiprocessing.cpu_count()
    # Set the total number of CPU's willing to use
    cpuuse = int(numcpu/2)
    print(f"Number of CPU's to be used is {cpuuse}")
    print("Hello?")

    # Create a process pool
    pool = multiprocessing.Pool(processes=cpuuse)
    processes = []

    # Set process name
    processname = "AlgorithmOne"
    # Create the process, and connect it to the worker function
    newprocess = multiprocessing.Process(target=AlgorithmImplementation.implementalgorithmone(), args=(0.5))
    # Add this to the list of processes for tracking purposes
    processes.append(newprocess)
    # Start the process
    # newprocess.start()

    # Set up the DataGathering process
    process_name = "DataGathering"
    # Create the process, connect it to the worker function
    new_process = multiprocessing.Process(target=datagathering.getexchangedata())
    # Add this to the list of processes for tracking purposes
    processes.append(new_process)
    # Start process
    # new_process.start()
    print(processes)

    for proc in processes:
        print(proc)
        proc.start()




