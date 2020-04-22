import pyfiglet
from datagathering import datagathering
from Trading import AlgorithmImplementation
import multiprocessing
from selfanalysis import dbanalysisclass
from selfanalysis import performanceanalysislibrary
from timeit import default_timer as timer
import time

# Function to remove worker process from jobs list
def removerworkerproc(ProcessName, jobs):
    # Find the index number in jobs list
    index = jobs.index(ProcessName)
    print(index)

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
    #binancetokens = AlgorithmImplementation.getallbinancetokens()
    # Add a list of tuples for binance coins to the total tokens to be analysed
    #for token in binancetokens["UniqueBinanceTokens"]:
    #    tokentuple = (token, "binance")
    #    tokenlist.append(tokentuple)
    return tokenlist


# Function to build in effective multiprocessor handling. Starting with handling incoming analysis results
def multiprocessor(CPUCores):
    # todo: this needs to be a lot more robust
    # Start timer
    start = timer()
    # Set up number of CPU Cores which can be used
    numCPUs = CPUCores
    # Get the list of tokens to be analysed
    tokenlist = []

    i = 0
    totaltokens = len(tokenlist)
    analyse = True
    while analyse == True:
        time.sleep(1)
        if i < totaltokens:
            # print("i is less than total tokens")
            # print(f"Number of CPUs is {numCPUs}")
            if numCPUs > 0:
                token = tokenlist[i][0]
                exchange = tokenlist[i][1]
                # Get the number of remaining tokens
                remainingtokens = totaltokens - i
                if i > 4:
                    # Small estimate on time remaining
                    timesofar = timer()
                    timetakensofar = (timesofar - 75) / i
                    timeremaining = remainingtokens * timetakensofar
                    print(
                        f'Analysing {token} from {exchange}. {i} tokens analysed, {remainingtokens} remain. Average time per token is {timetakensofar}, estimated time remaining is {timeremaining}')
                # Create the process to analyse the token
                proc = multiprocessing.Process(target=analysetoken, args=(token, exchange, outputqueue), name=token)
                # Add the process to processes list
                processes.append(proc)
                # Start the process
                proc.start()
                # Iterate to next token
                i = i + 1
                # Remove count of CPU to enable manual tracking etc
                numCPUs = numCPUs - 1
                print(f"Starting process {proc.name}")
            # Sleep for 1 second to allow everything to catchup
            elif numCPUs <= 0:
                msg = outputqueue.get()
                if msg != None:
                    print(f"Token analysed: {msg['Token']}")
                    for proc in processes:
                        print(f"Process currently being analysed: {proc.name}")
                        if proc.name == msg["Token"]:
                            index = processes.index(proc)
                            # print(f"Index of {proc.name} is {index}")
                            print(f"Terminating process: {proc.name}")
                            proc.terminate()
                            # Add in a new CPU to the count
                            numCPUs = numCPUs + 1
                            processes.pop(index)
        else:
            analyse = False



    end = timer()
    timetaken = end-start
    print(f'Function took {timetaken} seconds')
    for proc in processes:
        print(proc.name)


def getqueue(QueueObject):
    try:
        output = QueueObject.get()
    except:
        output = "NoDice"
    return output


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
    # Don't start automatically
    # algorithm.start()
    # Set up the initial analyse all tokens algorithm as I continue to test it
    # analysealgorithm = multiprocessing.Process(target=AlgorithmImplementation.testallcoinbasetokens, args=(), name="AlgorithmOneWargame")
    # jobs.append(analysealgorithm)
    # analysealgorithm.start()
    # multiprocessalgorithonewargaming(CPUCores)

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


