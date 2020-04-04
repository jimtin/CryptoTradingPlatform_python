import multiprocessing
import time
import datagathering
from Trading import AlgorithmImplementation

# Multiprocessing class to manage the multiple computations this program needs

class ParallelProcessing(multiprocessing.Process):
    def __init__(self,id):
        super(ParallelProcessing, self).__init__()
        self.id = id

    def run(self):
        print(f'Im the process with id: {self.id}')
        time.sleep(30)
        print("Completed")

    def datagathering(self):
        datagathering.getexchangedata()

    def algorithmone(self, Tolerance):
        AlgorithmImplementation.implementalgorithmone(Tolerance)
