from concurrent.futures import process
from typing import Any, Callable, List




class Core:
    def __init__(self, frequency: float, maxPowerConsumption: int, powerConsumptionFunction: Callable[[any , int], None] = None):
        self.frequency = frequency      # Processor frequency in Mhz.
        self.hertz = self.frequency * (1e6) # Processor frequency in Hertz.
        self.instructionsQueue: int = 0 # Number of instructions waiting for execution.
        self.temperature: float = 0     # Processor temperature in °C.
        self.currentPowerCosumption: float = 0  # Current power consumption in watts.
        self.maxPowerConsumption: int = maxPowerConsumption
        self.customPowerConsumptionFunction = powerConsumptionFunction  # # Custom function to calculate the temperature. It most update the currentPowerCosumption field.


    '''
        Executes one second of the processor and call the functions to set the temperature and the power consumption
        for the current workload.
    '''
    def Execute(self):
        instructionsToProcess = 0
        if self.instructionsQueue >= self.hertz:
            instructionsToProcess = self.hertz
            self.instructionsQueue -= self.hertz
        else:
            instructionsToProcess = self.instructionsQueue
            self.instructionsQueue = 0
        
        if self.customPowerConsumptionFunction == None:
            self.DefaultPowerConsumption(instructionsToProcess)
        else:
            self.customPowerConsumptionFunction(self, instructionsToProcess)
        
        return instructionsToProcess

    def DafaultTemperatureFunction(self, instructionsToProcess: int):
        self.temperature = self._Percentage(instructionsToProcess)


    def _Percentage(self, instructionsToProcess: int):
        return instructionsToProcess * 100 / self.hertz


    def DefaultPowerConsumption(self, instructionsToProcess: int):
        self.currentPowerCosumption = (self.maxPowerConsumption * self._Percentage(instructionsToProcess)) // 100

    
    def AddInstructionsToQueue(self, instructions: int):
        self.instructionsQueue += instructions


    def EstimatedTimeToCompletion(self):
        return self.instructionsQueue / self.hertz





