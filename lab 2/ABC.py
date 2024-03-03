import numpy as np
from functions import *

class ABC:
    def __init__(self, func, bounds, colony_size=30, max_iter=200, limit=100):
        self.func = func
        self.bounds = bounds
        self.colony_size = colony_size
        self.max_iter = max_iter
        self.limit = limit
        self.best_solution = None
        self.best_fitness = np.inf

    def optimize(self):
        dim = len(self.bounds)
        colony = np.random.uniform(low=self.bounds[:, 0], high=self.bounds[:, 1], size=(self.colony_size, dim))
        fitness = np.array([self.func(agent) for agent in colony])
        best_index = np.argmin(fitness)
        self.best_solution = colony[best_index]
        self.best_fitness = fitness[best_index]
        
        limit_counter = 0
        for _ in range(self.max_iter):
            if limit_counter > self.limit:
                break
            for i in range(self.colony_size):
                neighbor_index = np.random.choice([idx for idx in range(self.colony_size) if idx != i])
                phi = np.random.uniform(low=-1, high=1, size=dim)
                candidate = colony[i] + phi * (colony[i] - colony[neighbor_index])
                candidate = np.clip(candidate, self.bounds[:, 0], self.bounds[:, 1])
                candidate_fitness = self.func(candidate)
                if candidate_fitness < fitness[i]:
                    colony[i] = candidate
                    fitness[i] = candidate_fitness
                    limit_counter = 0
                else:
                    limit_counter += 1
            best_index = np.argmin(fitness)
            if fitness[best_index] < self.best_fitness:
                self.best_solution = colony[best_index]
                self.best_fitness = fitness[best_index]
        return self.best_solution, self.best_fitness
    

if __name__ == '__main__':
    abc = ABC(rosenbrock1, np.array([[-1.5, 1.5], [-0.5, 2.5]]), colony_size=30, max_iter=100)
    print(abc.optimize())
        
    abc = ABC(rosenbrock2, np.array([[-1.5, 1.5], [-1.5, 1.5]]), colony_size=30, max_iter=100)
    print(abc.optimize())

    abc = ABC(test_func, np.array([[0, 5], [0, 5]]), colony_size=30, max_iter=100)
    print(abc.optimize())

    abc = ABC(rastrigin, np.array([[-5.12, 5.12]]*10), colony_size=30, max_iter=100)
    print(abc.optimize())
