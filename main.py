import pyfiglet
from datagathering import datagathering
from Trading import AlgorithmImplementation
import multiprocessing
from selfanalysis import dbanalysisclass
from selfanalysis import performanceanalysislibrary
from timeit import default_timer as timer

# Function to remove worker process from jobs list
def removerworkerproc(ProcessName, jobs):
    # Find the index number in jobs list
    index = jobs.index(ProcessName)
    print(index)

# Function to get outputs from analysis
def analysetoken(Token, Exchange, Queue):
    outcome = AlgorithmImplementation.testtoken(Token, Exchange)
    Queue.put(outcome)


# Function to build in effective multiprocessor handling. Starting with handling incoming analysis results
def multiprocessalgorithonewargaming(CPUCores):
    # Start timer
    start = timer()
    # Set up number of CPU Cores which can be used
    numCPUs = CPUCores
    # Get the list of tokens to be analysed
    tokenlist = []
    # Notify user what we're doing
    print("Wargaming Algorithm One")
    # Get a list coinbase tokens
    coinbaselist = AlgorithmImplementation.getallcoinbasetokens()
    # Create list of tuples for coinbase tokens
    for token in coinbaselist["UniqueCoinbaseTokens"]:
        tokentuple = (token, "coinbase")
        tokenlist.append(tokentuple)
    # Get a list of binance tokens to analyse
    binancetokens = AlgorithmImplementation.getallbinancetokens()
    # Add a list of tuples for binance coins to the total tokens to be analysed
    for token in binancetokens["UniqueBinanceTokens"]:
        tokentuple = (token, "binance")
        tokenlist.append(tokentuple)
    # Give user some indication of the task which awaits.
    print(f'{len(tokenlist)} tokens to be analysed')
    # Setup queues
    outputqueue = multiprocessing.Queue()
    processes = []
    i = 0
    totaltokens = len(tokenlist)
    while i < len(tokenlist):
        token = tokenlist[i][0]
        exchange = tokenlist[i][1]
        if numCPUs > 0:
            # print(f'Next analysis target is Token: {token}, Exchange: {exchange}')
            # Create the process to analyse the token
            proc = multiprocessing.Process(target=analysetoken, args=(token, exchange, outputqueue), name=token)
            # Add the process to processes list
            processes.append(proc)
            # Start the process
            proc.start()
            # Iterate to next token
            i = i + 1
            # Kill a CPU from processing
            numCPUs = numCPUs - 1
        else:
            # Check to see if any processes are completed
            msg = outputqueue.get()
            if msg != None:
                for proc in processes:
                    if proc.name == msg["Token"]:
                        proc.terminate()
                        numCPUs = numCPUs + 1


    end = timer()
    timetaken = end-start
    print(f'Function took {timetaken} seconds')
    for proc in processes:
        print(proc.name)



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

    # Get the number of CPUs
    CPUCores = multiprocessing.cpu_count()
    # Subtract 1 for all other system process
    CPUCores = CPUCores - 1
    # Set up a list of processes
    jobs = []
    # First setup the self analysis process and confirm that mongodb is running

    # Setup Data gathering process
    data = multiprocessing.Process(target=datagathering.getexchangedata, args=(True,), name=datagatheringname)
    data.start()
    jobs.append(data)
    # This process must always be working, so subtract the CPU core
    CPUCores = CPUCores - 1

    # Now set up the Algorithm process
    algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(tolerance, True), name=algorithmname)
    jobs.append(algorithm)
    # Don't start automatically
    # algorithm.start()
    # Set up the initial analyse all tokens algorithm as I continue to test it
    # analysealgorithm = multiprocessing.Process(target=AlgorithmImplementation.testallcoinbasetokens, args=(), name="AlgorithmOneWargame")
    # jobs.append(analysealgorithm)
    # analysealgorithm.start()
    # multiprocessalgorithonewargaming(CPUCores)

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
        elif text == "wargamealgorithmone":
            multiprocessalgorithonewargaming(CPUCores)
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


