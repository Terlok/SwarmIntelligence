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
    #Path(f'{path}\GO').mkdir(parents=True, exist_ok=True)
    #Path(f'{path}\GO\Graph').mkdir(parents=True, exist_ok=True)
    #Path(f'{path}\GO\Animation').mkdir(parents=True, exist_ok=True)


class ACO_plot:
    def __init__(self, data, file_name) -> None:
        self.vavalues = data
        self.filename = file_name

    def graph(self, iter):
        x = self.values['points'][iter][0]
        x.append(self.values['points'][iter][0][0])
        y = self.values['points'][iter][1]
        y.append(self.values['points'][iter][1][0])
        plt.plot(x, y, linewidth=1)
        plt.scatter(x, y, s=math.pi * (math.sqrt(2.0) ** 2.0))
        for i in self.values['best_path'][iter]:
            plt.annotate(self.labels[i], self.data[i], size=8)
        
        plt.title(f'ACO. Min_max method')
        plt.savefig(f'{path}\ACO\Graph\{self.filename}.png')
        plt.close()

    def animation(self):
        fig, ax = plt.subplots(figsize=(8,6))

        x = self.values['points'][-1][0]
        x.append(self.values['points'][-1][0][0])
        y = self.values['points'][-1][1]
        y.append(self.values['points'][-1][1][0])

        ax.plot(x, y, linewidth=1)
        ax.scatter(x, y, s=math.pi * (math.sqrt(2.0) ** 2.0))
        ax.set_title('ACO. Min_max method')

        def animate(i):
            ax.clear()
            title = 'Iteration {:02d}'.format(i)
            ax.set_title(title)
            current_best_path = self.values['best_path'][i]  

            for j in range(len(current_best_path) - 1):
                node1 = current_best_path[j]
                node2 = current_best_path[j + 1]
                ax.plot([self.data[node1][0], self.data[node2][0]], [self.data[node1][1], self.data[node2][1]], linewidth=1, color='b')
                ax.scatter(self.data[node1][0], self.data[node1][1], s=math.pi * (math.sqrt(2.0) ** 2.0), color='r')
                ax.annotate(self.labels[node1], self.data[node1], size=8)

            last_node = current_best_path[-1]
            first_node = current_best_path[0]
            ax.plot([self.data[last_node][0], self.data[first_node][0]], [self.data[last_node][1], self.data[first_node][1]], linewidth=1, color='b')
            ax.scatter(self.data[last_node][0], self.data[last_node][1], s=math.pi * (math.sqrt(2.0) ** 2.0), color='r')
            ax.annotate(self.labels[last_node], self.data[last_node], size=8)

            for node in range(len(self.data)):
                ax.annotate(self.labels[node], self.data[node], size=8)

            return ax
        
        anim = FuncAnimation(fig, animate, frames=range(self.max_iter), interval=200, blit=False, repeat=False)
        anim.save(f'{path}\ACO\Animation\{self.filename}.gif', dpi=120, writer='pillow')

    