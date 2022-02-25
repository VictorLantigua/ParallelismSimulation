import copy
from typing import List, Set, Tuple
from core import Core
from random import choice, choices, randint, uniform
from simulation import *


class SimulationResult:
    def __init__(self, consumption: float, instructions: int, cpu: Tuple[int, ...]):
        self.consumption = consumption
        self.instructions = instructions
        self.cpu = cpu


def Schedule(cores: List[Core], instructions: int):
    cores = sorted(cores, key=lambda core: core.EstimatedTimeToCompletion())
    totalFrequency = sum([core.hertz for core in cores])
    percentages = [(core.hertz * 100) / totalFrequency for core in cores]

    assignedInstructions = 0
    for i in range(len(cores)):
        if instructions == 0:
            break
        selectedInstructions = (instructions * percentages[i]) // 100
        cores[i].AddInstructionsToQueue(selectedInstructions)
    
    return assignedInstructions


def MutateCPU(cpu: Tuple[int,...], numberOfMutations: int = 1, probability: float = 0.5):
    '''
    Mutates a CPU mutating a type of core into another.
    '''
    cpuList = list(cpu)
    for _ in range(numberOfMutations):
        if random() < probability:
            _indexA, _indexB = choices(population=range(len(cpu)), k=2)
            if cpuList[_indexA] > 0:
                cpuList[_indexA] -= 1
                cpuList[_indexB] += 1
    
    return tuple(cpuList)


def BalanceCPUCores(cpu: Tuple[int, ...], limit: int):
    '''
    Balances Cores in cpu to not have a lower or higher number of cores.
    '''
    total = sum(cpu)
    cpuLen = len(cpu)
    cpuList = list(cpu)
    while total > limit:
        _index = randint(0, cpuLen - 1)
        if cpuList[_index] > 0:
            cpuList[_index] -= 1
            total -= 1
    
    while total < limit:
        _index = randint(0, cpuLen - 1)
        cpuList[_index] += 1
        total += 1

    return tuple(cpuList)


def Pair(cpuA: Tuple[int, ...], cpuB: Tuple[int, ...]):
    '''
    Pairs two CPUs to create next-generation ones.
    '''
    _index = randint(1, len(cpuA) - 1)
    coresNumberLimit = sum(cpuA)
    nextCpuA = cpuA[0: _index] + cpuB[_index:]
    nextCpuB = cpuB[0: _index] + cpuA[_index:]

    nextCpuA = BalanceCPUCores(nextCpuA, coresNumberLimit)
    nextCpuB = BalanceCPUCores(nextCpuB, coresNumberLimit)

    return nextCpuA, nextCpuB



def SelectPair(population: List[SimulationResult]):
    '''
    Selcets a pair of CPUs from a list of processed SimilationResults with higher probabilities for better performance CPUs.
    '''
    weights = [cpu.instructions + 1 for cpu in population]
    return choices(population=population, weights=weights, k=2)


def GetInitialPopulation(coresPerCPU: int, availableCores: int, numberOfGenomes: int):
    cpuList = set()

    while len(cpuList) < numberOfGenomes:
        currentCPU = [0 for _ in range(availableCores)] # List to track the number of each core for the current cpu.
        coresCounter = 0
        '''
        Uniformly generates random indexes to select what kind of core is going to be selected for each cell.
        The selected index is set to true, and we repeat the process until we get the desired amount of cores selected.
        '''
        for _ in range(coresPerCPU):
            currentSelection = int(uniform(0, 1) * availableCores)
            currentCPU[currentSelection] += 1
            coresCounter += 1
        
        cpuList.add(tuple(currentCPU))
    
    return cpuList


def GetCpuFromSelectionTuple(cores: List[Core], selectionTuple: Tuple[int, ...]):
    '''
    Returns a list of cores from a tuple that stores the amount of each core from the list.
    '''
    cpu = []
    for i in range(len(cores)):
        for counter in range(selectionTuple[i]):
            cpu.append(copy.deepcopy(cores[i]))
    
    return cpu


def GetNextGeneration(currentGeneration: List[SimulationResult]):
    pass


def CpuArchitectureGeneticAlgorithm(cores: List[Core], numberOfCores: int, consumptionLimit: float, generationLimit: int, numberOfGenomes: int):
    # lenOfSystem = numberOfCores * len(cores)
    # listOfCPUs = set()
    
    # Here we generate an initial population.
    # while len(listOfCPUs) < 16:
    #     currentCPU = [0 for _ in range(len(cores))] # List to track the number of each core for the current cpu.
    #     coresCounter = 0
    #     '''
    #     Uniformly generate random indexes to select what kind of core is going to be selected for each cell.
    #     The selected index is set to true, and we repeat the process until we get the desired amount of cores selected.
    #     '''
    #     while coresCounter < numberOfCores:
    #         currentSelection = int(uniform(0, 1) * len(cores))
    #         currentCPU[currentSelection] += 1
    #         coresCounter += 1
        
    #     listOfCPUs.add(tuple(currentCPU))

    currentGeneration: Set[Tuple[int,...]] = GetInitialPopulation(numberOfCores, len(cores), numberOfGenomes)

    bestCPU: SimulationResult = None
    for _ in range(generationLimit):
        currentGenerationSolutions: List[SimulationResult] = []
        for cpu in currentGeneration:   # Evaluates current generation.
            currentCPU: List[Core] = GetCpuFromSelectionTuple(cores, cpu)
            currentSimulation = ParallelismSimulation(24, currentCPU, Schedule)
            currentSimulation.RunSimulation()
            currentConsumption = sum(currentSimulation.cumulativeConsumption)
            currentInstructions = currentSimulation.processedInstructions if currentConsumption < consumptionLimit else 0
            currentGenerationSolutions.append(SimulationResult(currentConsumption, currentInstructions, cpu))
        
        currentGenerationSolutions = sorted(currentGenerationSolutions, key=lambda sol: sol.instructions, reverse=True)
        
        if bestCPU == None or bestCPU.instructions < currentGenerationSolutions[0].instructions:
            bestCPU = currentGenerationSolutions[0]
        
        # Select best CPUs to be in the next generation (Elitism).
        nextGeneration = [solution.cpu for solution in currentGenerationSolutions[:2]]

        # Execute pair and mutation.
        for _ in range(int(len(currentGenerationSolutions) / 2) - 1):
            cpuA, cpuB = SelectPair(currentGenerationSolutions)
            nextCpuA, nextCpuB = Pair(cpuA.cpu, cpuB.cpu)
            nextGeneration.append(nextCpuA)
            nextGeneration.append(nextCpuB)
        
        currentGeneration = nextGeneration

    return bestCPU