from CPUs import *
from ProcessorGeneticAlgorithm import *
import matplotlib.pyplot as plt


def main():
    cores = [coreA, coreB, coreC, coreD, coreE, coreF]
    results = []
    for _ in range(100):
        best = CpuArchitectureGeneticAlgorithm(cores, 24, 3000, 100, 18)
        results.append(best.instructions)
        print(f'cpu {best.cpu}')
        print(f'consumption {best.consumption}')
        print(f'instructions {best.instructions}')
    
    plt.plot(range(100), results)
    plt.show()

    


if __name__ == "__main__":
    main()