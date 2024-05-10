from os import mkdir
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = Path(__file__).parent.resolve()

def create_folders():
    Path(f'{path}\\DE').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\\DE\\Animation').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\\PSO').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\\PSO\\Animation').mkdir(parents=True, exist_ok=True)

class Visualizer:
    def __init__(self, algorithm, data, file_name, max_iter=None) -> None:
        self.alg = algorithm
        self.data = data
        self.filename = file_name
        self.max_iter = max_iter

    def distance(self, ):
        fitness = self.data['fit']
        best_fitness = [max(iteration) for iteration in fitness]
        plt.plot(range(1, len(best_fitness) + 1), best_fitness)
        plt.xlabel('Iteration')
        plt.ylabel('Best fitness')
        plt.title('Evolution best of fitness')
        plt.grid(True)
        plt.savefig(f'{path}\\{self.alg}\\{self.filename}.png')
        plt.close()