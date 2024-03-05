import numpy as np
from functions import reducer_weight

class FireflyAlgorithm:
    def __init__(self, function, colony_size=30, bounds=None, max_iter=200, alpha=0.2, beta=1, gamma=1):
        self.function = function
        self.bounds = bounds
        self.colony_size = colony_size
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.values = {'pop':[], 'fitness': []}

    def __create_vector__(self):
        points = []
        if self.function != reducer_weight:
            for i in range(len(self.bounds)):
                points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) for _ in range(self.colony_size)])
        else:
            for i in range(len(self.bounds)):
                points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) if j != 2 else int(np.random.uniform(self.bounds[i][0], self.bounds[i][1])) for j in range(self.colony_size)])
        return np.array(points).T

    def optimize(self):
        population = self.__create_vector__()
        fitness = np.apply_along_axis(self.function, 1, population)

        for _ in range(self.max_iter):
            for i in range(self.colony_size):
                for j in range(self.colony_size):
                    if fitness[j] < fitness[i]:
                        distance = np.linalg.norm(population[i] - population[j])
                        attractiveness = np.exp(-self.gamma * distance**2)
                        population[i] += self.alpha * attractiveness * (population[j] - population[i]) + self.beta * (np.random.rand(len(self.bounds)) - 0.5)

                for dim in range(len(self.bounds)):
                    population[i][dim] = np.maximum(self.bounds[dim][0], population[i][dim])
                    population[i][dim] = np.minimum(self.bounds[dim][1], population[i][dim])

            fitness = np.apply_along_axis(self.function, 1, population)
            self.values['pop'].append(population.T.copy())
            self.values['fitness'].append(fitness.copy())
            best_index = np.argmin(fitness)
            best_solution = population[best_index]
            best_fitness = fitness[best_index]

        return best_solution, best_fitness