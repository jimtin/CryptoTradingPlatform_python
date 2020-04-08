from selfanalysis import performanceanalysisclasses

# Library of functions across various performance related aspects. Goal will be to implement these into a separate analysis thread in main
def getperformanceoffunctions(TimeFrame):
    # Get the performance of the datagathering library over time
    datagatheringtime = performanceanalysisclasses.FunctionTimes("getexchangedata").getaveragetime(TimeFrame)
    print(f"Average datagathering time over {TimeFrame} hours is {datagatheringtime} seconds")
    algorithmonetime = performanceanalysisclasses.FunctionTimes("implementalgorithmone").getaveragetime(TimeFrame)
    print(f"Average time for algorithm one to run in past {TimeFrame} hours is {algorithmonetime} seconds")
