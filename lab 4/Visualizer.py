import math
import numpy as np
from os import mkdir
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = Path(__file__).parent.resolve()

def create_folders():
    Path(f'{path}\ACO').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\ACO\Graph').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\ACO\Animation').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\ACO\Distance').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\GO').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\GO\Graph').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\GO\Animation').mkdir(parents=True, exist_ok=True)
    Path(f'{path}\GO\Distance').mkdir(parents=True, exist_ok=True)


class Visualizer:
    def __init__(self, algo, data, values, labels, file_name, max_iter) -> None:
        self.algo = algo
        self.data = data
        self.values = values
        self.labels = labels
        self.filename = file_name
        self.max_iter = max_iter

    def best_route(self, iter):
        x = self.values['points'][iter][0]
        x.append(self.values['points'][iter][0][0])
        y = self.values['points'][iter][1]
        y.append(self.values['points'][iter][1][0])
        plt.plot(x, y, linewidth=1)
        plt.scatter(x, y, s=5)
        for i in self.values['best_path'][iter]:
            plt.annotate(self.labels[i], self.data[i], size=8)
        
        plt.title('Best Route')
        plt.savefig(f'{path}\{self.algo}\Graph\{self.filename}.png')
        plt.close()

    def animation(self):
        fig, ax = plt.subplots(figsize=(8,6))

        x = self.values['points'][-1][0]
        x.append(self.values['points'][-1][0][0])
        y = self.values['points'][-1][1]
        y.append(self.values['points'][-1][1][0])

        ax.plot(x, y, linewidth=1)
        ax.scatter(x, y, s=5)
        ax.set_title('Animation')

        def animate(i):
            ax.clear()
            title = 'Iteration {:02d}'.format(i)
            ax.set_title(title)
            current_best_path = self.values['best_path'][i]  

            for j in range(len(current_best_path) - 1):
                node1 = current_best_path[j]
                node2 = current_best_path[j + 1]
                ax.plot([self.data[node1][0], self.data[node2][0]], [self.data[node1][1], self.data[node2][1]], linewidth=1, color='b')
                ax.scatter(self.data[node1][0], self.data[node1][1], s=5, color='blue')
                ax.annotate(self.labels[node1], self.data[node1], size=8)

            last_node = current_best_path[-1]
            first_node = current_best_path[0]
            ax.plot([self.data[last_node][0], self.data[first_node][0]], [self.data[last_node][1], self.data[first_node][1]], linewidth=1, color='b')
            ax.scatter(self.data[last_node][0], self.data[last_node][1], s=5, color='blue')
            ax.annotate(self.labels[last_node], self.data[last_node], size=8)

            for node in range(len(self.data)):
                ax.annotate(self.labels[node], self.data[node], size=8)

            return ax
        
        if len(self.values['points']) <= 50:
            anim = FuncAnimation(fig, animate, frames=range(self.max_iter), interval=200, blit=False, repeat=False)
        else:
            anim = FuncAnimation(fig, animate, frames=range(0, len(self.values['points']), int(len(self.values['points'])/self.max_iter)), interval=200, blit=False, repeat=False)
        
        anim.save(f'{path}\{self.algo}\Animation\{self.filename}.gif', dpi=120, writer='pillow')
        plt.close()

    def distance(self):
        distances = self.values['distance']
        plt.plot(range(len(distances)), distances, linestyle='-')
        plt.title('Distance per Epoch')
        plt.xlabel('Epochs')
        plt.ylabel('Distance')
        plt.savefig(f'{path}\{self.algo}\Distance\{self.filename}.png')
        plt.close()