import numpy as np
from os import mkdir
from graphics import *
from functions import *
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = Path(__file__).parent.resolve()

def create_folders():
    Path(f'{path}\Scatter plot').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\Animation').mkdir(parents=True, exist_ok=True)

class Animation:
    def __init__(self, filename:str, interval:list, function:str, values:dict) -> None:
        self.filename = filename
        self.interval = interval
        self.function = function
        self.values = values

    def animate(self) -> None:
        x, y = np.array(np.meshgrid(np.linspace(self.interval[0][0], self.interval[0][1], 100), np.linspace(self.interval[1][0], self.interval[1][1], 100)))
        z = self.function(x, y)

        x_min = x.ravel()[z.argmin()]
        y_min = y.ravel()[z.argmin()]
    
        fig, ax = plt.subplots(figsize=(8,6))
        fig.set_tight_layout(True)
        img = ax.imshow(z, extent=[self.interval[0][0], self.interval[0][1], self.interval[1][0], self.interval[1][1]], origin='lower', cmap='viridis', alpha=0.5)
        fig.colorbar(img, ax=ax)
        ax.plot([x_min], [y_min], marker='x', markersize=5, color="white")
        contours = ax.contour(x, y, z, 10, colors='black', alpha=0.4)
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.0f")

        pbest_plot = ax.scatter(self.values['pbest'][0], self.values['pbest'][1], marker='o', color='black', alpha=0.5)
        p_plot = ax.scatter(self.values['X'][0], self.values['X'][1], marker='o', color='blue', alpha=0.5)

        def animate(i):
            title = 'Iteration {:02d}'.format(i)
            ax.set_title(title)
            pbest_plot.set_offsets(self.values['pbest'][i].T)
            p_plot.set_offsets(self.values['X'][i].T)
            
            return ax, pbest_plot, p_plot

        anim = FuncAnimation(fig, animate, frames=len(self.values['X']), interval=200, blit=False, repeat=False)
        anim.save(f'{path}\Animation\{self.filename}.gif', dpi=120, writer='pillow')

def scatter_plot(function_name, values):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(function_name)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    ax.scatter([i[0] for i in values['pop']], [i[1] for i in values['pop']], values['fitness'], color='red')
    plt.savefig(f'{path}\Scatter plot\{function_name}.png')