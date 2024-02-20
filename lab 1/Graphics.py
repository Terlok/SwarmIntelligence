import numpy as np
from os import mkdir
from pathlib import Path
import matplotlib.pyplot as plt
path = Path(__file__).parent.resolve()

def create_folders():
    Path('FitnessTrend').mkdir(parents=True, exist_ok=True)
    Path('Distances').mkdir(parents=True, exist_ok=True)
    Path('Animation').mkdir(parents=True, exist_ok=True)

def fitness_trend(filename:str, fit:list):
    fitness = np.array(fit)
    fitness = fitness.T
    fig = plt.figure()
    for i in range(len(fitness)):
        plt.plot(fitness[i])
    plt.xlabel('epoch')
    plt.ylabel('fitness')
    plt.title('Fitness of population')
    plt.savefig(f'{path}\FitnessTrend\{filename}_fit_trend_.png')
    plt.close(fig)

def distances(filename:str, best:list):
    fig = plt.figure()
    distance = np.diff(best)
    plt.plot(distance)
    plt.xlabel('epoch')
    plt.ylabel('distance')
    plt.title('Distance')
    plt.savefig(f'{path}\Distances\{filename}_distances.png')
    plt.close(fig)

