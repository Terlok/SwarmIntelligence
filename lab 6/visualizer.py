import numpy as np
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
    def __init__(self, algorithm, file_name, data, b_values=None, max_iter=None) -> None:
        self.alg = algorithm
        self.filename = file_name
        self.data = data
        self.max_iter = max_iter

    def animation(self):
        fig = plt.figure()

        def update(frame):
            plt.cla()
            fitness = self.data['fit']
            best_fitness = [max(iteration[:frame+1]) for iteration in fitness[:frame+1]]
            plt.plot(range(1, len(best_fitness) + 1), best_fitness)
            plt.xlabel('Iteration')
            plt.ylabel('Best fitness')
            plt.title('Evolution best of fitness')
            plt.title(f'Iteration {frame}')
            plt.grid(True)

        fig, ax = plt.subplots()

        if len(self.data['fit']) <= 100:
            ani = FuncAnimation(fig, update, frames=len(self.data['fit']), blit=False, repeat=False)
        else:
            ani = FuncAnimation(fig, update, frames=range(0, len(self.data['fit']), int(len(self.data['fit']) / self.max_iter)), interval=200, blit=False, repeat=False)

        ani.save(f'{path}\\{self.alg}\\Animation\\{self.filename}.gif', dpi=120, writer='pillow')
        plt.close()

    def plot_fitness(self):
        fitness = self.data['fit']
        best_fitness = [max(iteration) for iteration in fitness]
        plt.plot(range(1, len(best_fitness) + 1), best_fitness)
        plt.xlabel('Iteration')
        plt.ylabel('Best fitness')
        plt.title('Evolution best of fitness')
        plt.grid(True)
        plt.savefig(f'{path}\\{self.alg}\\{self.filename}.png')
        plt.close()