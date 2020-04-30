import pyfiglet
from datagathering import datagathering
from Trading import AlgorithmImplementation
import multiprocessing
from selfanalysis import performanceanalysislibrary
import time



# Function to get outputs from analysis
def analysetoken(Token, Exchange, Queue):
    # Get data for token
    outcome = AlgorithmImplementation.testtoken(Token=Token, Exchange=Exchange, ProcessName=Token)
    procname = f"{Token}Process"
    proccomplete = {
        "ProcessName": procname,
        "Status": "Completed",
        "Outcome": outcome
    }
    Queue.put(proccomplete)


# Function to get a list of unique tokens currently held in database
def gettokenlist():
    # Set up list to store token and exchange
    tokenlist = []
    # Get the coinbase list
    coinbaselist = AlgorithmImplementation.getallcoinbasetokens()
    # Convert into a list of tuples for coinbase
    for token in coinbaselist["UniqueCoinbaseTokens"]:
        tokentuple = (token, "coinbase")
        tokenlist.append(tokentuple)
    # Get a list of binance tokens to analyse
    binancetokens = AlgorithmImplementation.getallbinancetokens()
    # Add a list of tuples for binance coins to the total tokens to be analysed
    for token in binancetokens["UniqueBinanceTokens"]:
        tokentuple = (token, "binance")
        tokenlist.append(tokentuple)
    return tokenlist


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
    # Set up the process queue
    outputqueue = multiprocessing.Queue()
    # Set up a list of processes
    processes = []


    # Always start the datagathering process
    data = multiprocessing.Process(target=datagathering.getexchangedata, args=(True,), name=datagatheringname)
    data.start()
    processes.append(data)
    # This process must always be working, so subtract the CPU core
    CPUCores = CPUCores - 1
    # Notify user
    print(f"Starting datagathering process. Process name: {processes[0].name}")


    # Now set up the Algorithm process
    algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(tolerance, True), name=algorithmname)
    processes.append(algorithm)

    # Set up an iterator
    i = 0
    # Set up a token list
    tokenlist = []
    # Set up a CPUFlag variable
    CPUFlag = ""

    runprogram = True

    # Wait for user input
    while runprogram == True:
        time.sleep(0.5)
        # CPU Flag assessment
        if CPUFlag == "wargamealgorithmone":
            if i < len(tokenlist):
                if CPUCores > 0:
                    if len(tokenlist) >= 1:
                        if i < len(tokenlist):
                            nexttoken = tokenlist[i][0]
                            exchange = tokenlist[i][1]
                            procname = f"{nexttoken}Process"
                            print(f"Starting analysis of {nexttoken}, total number of tokens analysed is {i}")
                            # Create the process to analyse token
                            proc = multiprocessing.Process(target=analysetoken, args=(nexttoken, exchange, outputqueue),
                                                           name=procname)
                            # Add the process to the list
                            processes.append(proc)
                            # Start the process
                            proc.start()
                            # Increment i
                            i = i + 1
                            # Decrement number of CPU cores available
                            CPUCores = CPUCores - 1
                else:
                    if outputqueue.empty():
                        continue
                    else:
                        msg = outputqueue.get()
                        if msg["Status"] == "Completed":
                            print(f"Analysis of {msg['ProcessName']} completed")
                            # Terminate the process which was doing analysis and remove from processes list
                            for object in processes:
                                if object.name == msg["ProcessName"]:
                                    object.terminate()
                                    # Get the index of the object
                                    index = processes.index(object)
                                    # Pop from the list
                                    processes.pop(index)
                                    # Add another CPU to the count
                                    CPUCores = CPUCores + 1
            else:
                CPUFlag = ""
                # todo: clean up the last four processes once they complete
        else:
            text = input('Input command: ')
            # text = "wargamealgorithmone"
            if text == 'performance':
                # Setup a process to get the status
                performanceanalysislibrary.getperformanceoffunctions(24)
            elif text == 'status':
                # Query the jobs list to check on status
                for proc in processes:
                    print(f'Process Name: {proc.name}')
                    print(f'Process Status: {proc.is_alive()}')
                    print(f'Process PID: {proc.pid}')
            elif text == "wargamealgorithmone":
                # Check if we've already started the wargame algorithm
                if CPUFlag == "wargamealgorithim":
                    continue
                else:
                    CPUFlag = "wargamealgorithmone"
                    # Notify user what we're doing
                    print("Wargaming Algorithm One")
                    print(f"Number of CPUs available: {CPUCores}")
                    # If list of tokens not yet gathered, get them
                    if len(tokenlist) == 0:
                        # Let user know what we're doing
                        print(f"Getting a list of tokens")
                        # Get a list of tokens to be analysed
                        tokenlist = gettokenlist()
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
                processes.remove(algorithm)
                algorithm = multiprocessing.Process(target=AlgorithmImplementation.iteralgorithms, args=(tolerance, True),
                                                    name=algorithmname)
                processes.append(algorithm)
                algorithm.start()
            elif text == 'q':
                # Notify user that you are exiting the program
                print("Exiting program")
                # Send terminate command to all processes. Not pretty or graceful but will work on that later
                for proc in processes:
                    proc.terminate()
                    runprogram = False
            else:
                print("Invalid text")


