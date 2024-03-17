import numpy as np
import random as rnd
from math import gamma

class cso:
    def __init__(self, function, pop_size, bounds, max_iter=200, pa=0.25, nests_count=50):
        self.function = function
        self.pop_size = pop_size
        self.bounds = bounds
        self.max_iter = max_iter
        self.pa = pa
        self.nests_count = nests_count

        self.cuckoos = self.__create__(self.pop_size)
        self.nests = self.__create__(self.nests_count)

        self.values = {'pop': [], 'fitness': []}
        self.nests_values = {'pop': [], 'fitness': []}

        beta = 3 / 2
        sigma = (gamma(1 + beta) * np.sin(np.pi * beta / 2) / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        u = np.array([rnd.normalvariate(0, 1) for _ in range(len(self.bounds))]) * sigma
        v = np.array([rnd.normalvariate(0, 1) for _ in range(len(self.bounds))])
        self.step = u / abs(v) ** (1 / beta)

    def __create__(self, size):
        points = []
        for i in range(len(self.bounds)):
            points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) if j != 2 else int(np.random.uniform(self.bounds[i][0], self.bounds[i][1])) for j in range(size)])
        return np.array(points)
    
    def __layingEggs__(self, random_index, value_index):
        for list_index in range(len(self.cuckoos)):
            self.nests[list_index][random_index] = self.cuckoos[list_index][value_index]

    def __getPbest__(self):
        index_of_min_fitness = np.argmin(self.values['fitness'][-1])
        return self.values['fitness'][-1][index_of_min_fitness]

    def __levyfly__(self):
        combined = list(zip(*self.cuckoos))
        for i in range(len(combined)):
            stepsize = 0.2 * self.step * (self.values['fitness'][-1][i] - self.__getPbest__())
            combined[i] += stepsize * np.array([rnd.normalvariate(0, 1) for _ in range(len(self.bounds))])
        self.cuckoos = list(map(list, zip(*combined)))
            
    def execute(self):
        for _ in range(self.max_iter):
            self.values['pop'].append(self.cuckoos)
            self.values['fitness'].append(self.function(self.cuckoos))
            self.nests_values['pop'].append(self.nests)
            self.nests_values['fitness'].append(self.function(self.nests))

            for value_index in range(len(self.cuckoos[0])):
                random_index = rnd.randint(0, len(self.nests[0]) - 1)
                if self.values['fitness'][-1][value_index] < self.nests_values['fitness'][-1][random_index] and rnd.random() > self.pa:
                    self.__layingEggs__(random_index, value_index)
                else:
                    self.__layingEggs__(random_index, 0)

            self.__levyfly__()
            

from functions import *

if __name__ == '__main__':
    #test = cso(mishras_bird, pop_size=150, max_iter=500, bounds=[[-10, 0], [-6.5, 0]], nests_count=200, pa=0.75)
    #test = cso(rastrigin, pop_size=5, bounds=[[-5.12, 5.12]]*2, nests_count=200, pa=0.75)
    test = cso(rosenbrock1, pop_size=150, max_iter=500, bounds=[[-1.5, 1.5], [-0.5, 2.5]], nests_count=200, pa=0.75)
    
    test.execute()
    #print(min(test.values['fitness'][-1]))
    #print(test.values['pop'])
    print(min(test.values['fitness'][-1]))






