import numpy as np
from os import mkdir
from graphics import *
from functions import *
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = Path(__file__).parent.resolve()

def create_folders():
    Path(f'{path}\FitnessTrend').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\Distances').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\Animation').mkdir(parents=True, exist_ok=True)

class Animation:
    def __init__(self, filename:str, bounds:list, function:str, values:dict) -> None:
        self.filename = filename
        self.bounds = bounds
        self.function = function
        self.values = values

    def animate(self) -> None:
        x, y = np.array(np.meshgrid(np.linspace(self.bounds[0][0], self.bounds[0][1], 100), np.linspace(self.bounds[1][0], self.bounds[1][1], 100)))
        z = self.function([x, y])

        x_min = x.ravel()[z.argmin()]
        y_min = y.ravel()[z.argmin()]
    
        fig, ax = plt.subplots(figsize=(8,6))
        fig.set_tight_layout(True)
        img = ax.imshow(z, extent=[self.bounds[0][0], self.bounds[0][1], self.bounds[1][0], self.bounds[1][1]], origin='lower', cmap='viridis', alpha=0.5)
        fig.colorbar(img, ax=ax)
        
        ax.plot([x_min], [y_min], marker='x', markersize=5, color="white")
        p_plot = ax.scatter(self.values['pop'][0], self.values['pop'][1], marker='o', alpha=0.5, color='green')

        def animate(i):
            title = 'Iteration {:02d}'.format(i)
            ax.set_title(title)
            p_plot.set_offsets(self.values['pop'][i].T)
            
            return ax, p_plot

        anim = FuncAnimation(fig, animate, frames=range(0, len(self.values['pop']), int(len(self.values['pop'])/50)), interval=200, blit=False, repeat=True)
        anim.save(f'{path}\Animation\{self.filename}.gif', dpi=120, writer='pillow')

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
