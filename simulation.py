from typing import Callable, List
from core import Core
from distributions import *


class ParallelismSimulation:
    
    def __init__(self, simulationTimeInSeconds: int, cores: List[Core], scheduler: Callable[[List[Core], int], None], meanInstructionsPerSecond: float = 1e-180):
        self.currentTime = 0    # Current moment of the simulation in seconds.
        self.instructionsQueue = 0  # Number of instructions waiting to be processed.
        self.processedInstructions = 0  # Number of processed instructions.
        self.cumulativeConsumption = [0 for i in cores] # Power consumption per core per second.
        self.processedInstructionsPerCore = [0 for i in cores]  # Processed instructions per core.

        self.meanInstructionsPerSecond = meanInstructionsPerSecond
        self.totalTime = simulationTimeInSeconds  # Total time of the simulation in seconds.
        self.cores = cores
        self.Scheduler = scheduler

    '''
        Simulate a second of the system.
    '''
    def Simulate(self):
        # Executes a second on every core or the system.
        for i in range(len(self.cores)):
            instructions = self.cores[i].Execute()
            self.processedInstructionsPerCore[i] += instructions
            self.cumulativeConsumption[i] += self.cores[i].currentPowerCosumption
            self.processedInstructions += instructions

        instructions = Exponential(self.meanInstructionsPerSecond)
        self.instructionsQueue += int(instructions)
        scheduled = self.Scheduler(self.cores, self.instructionsQueue)
        self.instructionsQueue -= scheduled

    
    def RunSimulation(self):
        self.ResetSimulation()
        for _ in range(self.totalTime):
            self.Simulate();

    
    def ResetSimulation(self):
        self.currentTime = 0
        self.instructionsQueue = 0
        self.processedInstructions = 0
        self.cumulativeConsumption = [0 for i in self.cores]
        self.processedInstructionsPerCore = [0 for i in self.cores]