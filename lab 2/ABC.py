import numpy as np

class ABC:
    def __init__(self, func, bounds, colony_size=30, max_iter=200, limit=100) -> None:
        self.func = func
        self.bounds = bounds
        self.colony_size = colony_size
        self.max_iter = max_iter
        self.limit = limit
        self.best_solution = None
        self.best_fitness = np.inf  
        self.values = {'pop':[], 'fitness': []}

    def __create_vector__(self):
        points = []
        for i in range(len(self.bounds)):
            points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) for _ in range(self.colony_size)])
        return np.array(points)

    def optimize(self):
        dim = len(self.bounds)
        colony = self.__create_vector__()
        fitness = np.array([self.func(agent) for agent in colony.T])  
        best_index = np.argmin(fitness)
        self.best_solution = colony[:, best_index]
        self.best_fitness = fitness[best_index]
        
        limit_counter = 0
        for _ in range(self.max_iter):
            if limit_counter > self.limit:
                break
            for i in range(self.colony_size):
                neighbor_index = np.random.choice([idx for idx in range(self.colony_size) if idx != i])
                phi = np.random.uniform(low=-1, high=1, size=dim)
                candidate = colony[:, i] + phi * (colony[:, i] - colony[:, neighbor_index])
                candidate = np.clip(candidate, self.bounds[:, 0], self.bounds[:, 1])
                candidate_fitness = self.func(candidate)
                if candidate_fitness < fitness[i]:
                    colony[:, i] = candidate
                    fitness[i] = candidate_fitness
                    limit_counter = 0
                else:
                    limit_counter += 1

                self.values['pop'].append(colony)
                self.values['fitness'].append(fitness)
            best_index = np.argmin(fitness)
            if fitness[best_index] < self.best_fitness:
                self.best_solution = colony[:, best_index]
                self.best_fitness = fitness[best_index]
        return self.best_solution, self.best_fitness    



from functions import *
from graphics import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    # abc2 = ABC(mishras_bird, np.array([[-10, 0], [-6.5, 0]]), colony_size=30)

    # best_solution, best_fitness = abc2.optimize()
    # print(f'Best solution is: {best_solution}')
    # print(f'Best fitness is: {best_fitness}')

    abc5 = ABC(simionescu, np.array([[-1.25, 1.25], [-1.25, 1.25]]), colony_size=30)

    best_solution, best_fitness = abc5.optimize()
    print(f'Best solution is: {best_solution}')
    print(f'Best fitness is: {best_fitness}')


    # abc2 = ABC(rosenbrock1, np.array([[-1.5, 1.5], [-0.5, 2.5]]), colony_size=30)

    # best_solution, best_fitness = abc2.optimize()
    # print(f'Best solution is: {best_solution}')
    # print(f'Best fitness is: {best_fitness}')

    x = np.linspace(-1.25, 1.25, 100)
    y = np.linspace(-1.25, 1.25, 100)
    X, Y = np.meshgrid(x, y)
    Z = mishras_bird([X, Y])

    # Create a 3D plot of the Rastrigin function
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

    