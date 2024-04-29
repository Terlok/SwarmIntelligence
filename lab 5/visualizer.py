from os import mkdir
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = Path(__file__).parent.resolve()

def create_folders():
    Path(f'{path}\\GA').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\\GA\\Animation').mkdir(parents=True, exist_ok=True)

class Visualizer:
    def __init__(self, data, file_name, max_iter=None) -> None:
        self.data = data
        self.filename = file_name
        self.max_iter = max_iter

    def animation(self):
        chromosomes = self.data['pop']
        fitness = self.data['fit']

        def update(frame):
            plt.cla()
            current_chromosomes = chromosomes[frame]
            current_fitness = fitness[frame]
            
            sns.barplot(x=current_chromosomes, y=current_fitness)
            
            plt.xlabel('Chromosomes')
            plt.ylabel('Fitness value')
            plt.title(f'Iteration {frame}')

        fig, ax = plt.subplots()

        if len(self.data['pop']) <= 100:
            ani = FuncAnimation(fig, update, frames=len(chromosomes), blit=False, repeat=False)
        else:
            ani = FuncAnimation(fig, update, frames=range(0, len(self.data['pop']), int(len(self.data['pop']) / self.max_iter)), interval=200, blit=False, repeat=False)

        ani.save(f'{path}\\GA\\Animation\\{self.filename}.gif', dpi=120, writer='pillow')
        plt.close()

    def distance(self):
        fitness = self.data['fit']
        best_fitness = [max(iteration) for iteration in fitness]
        plt.plot(range(1, len(best_fitness) + 1), best_fitness, marker='o', markersize=4)
        plt.xlabel('Iteration')
        plt.ylabel('Best fitness value over iteration')
        plt.title('Best fitness value')
        plt.grid(True)
        plt.savefig(f'{path}\\GA\\{self.filename}.png')
        plt.close()