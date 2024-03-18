import numpy as np
import random as rnd
from math import gamma

class cso:
    def __init__(self, function, pop_size, bounds, max_iter=200, pa=0.25, stepSize=0.01, nests_count=50):
        self.function = function
        self.pop_size = pop_size
        self.bounds = bounds
        self.max_iter = max_iter
        self.pa = pa
        self.stepSize = stepSize
        self.nests_count = nests_count

        self.cuckoos = self.__create__(self.pop_size)
        self.nests = self.__create__(self.nests_count)

        self.values = {'pop': [], 'fitness': []}
        self.nests_values = {'pop': [], 'fitness': []}

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
    
    def __levyFlight__(self):
        Lambda=1.5
        sigma1=np.power((gamma(1+Lambda) * np.sin((np.pi*Lambda) / 2)) \
            / gamma((1+Lambda) / 2) * np.power(2,(Lambda-1) / 2),1 / Lambda)
        sigma2=1
        u=np.random.normal(0,sigma1,size=len(self.bounds))
        v=np.random.normal(0,sigma2,size=len(self.bounds))
        step=u/np.power(np.fabs(v),1/Lambda)
        return  step
    
    def __newGen__(self):
        combined = list(zip(*self.cuckoos))
        for i in range(len(combined)):
            combined[i] += self.__levyFlight__() * combined[i] * self.stepSize
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

            self.__newGen__()