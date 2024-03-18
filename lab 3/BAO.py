import numpy as np
import random as rnd

class bao:
    def __init__(self, function, pop_size, bounds, max_iter=200, A=0.5, r=0.5, Qmin=-2, Qmax=2):
        self.function = function
        self.pop_size = pop_size  #population size 
        self.bounds = bounds
        self.max_iter = max_iter  #generations
        self.A = A  #loudness
        self.r = r  #pulse rate
        self.Qmin = Qmin  #frequency min
        self.Qmax = Qmax  #frequency max

        self.bats = self.__initPopulation__()         
        self.Q = None  #frequency
        self.velocity = [[0 for _ in range(self.pop_size)] for _ in range(len(self.bounds))]  #velocity

        self.values = {'pop': [], 'fitness': []}

    def __initPopulation__(self):
        points = []
        for i in range(len(self.bounds)):
            points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) if j != 2 else int(np.random.uniform(self.bounds[i][0], self.bounds[i][1])) for j in range(self.pop_size)])
        return np.array(points)
    
    def __setFrequency__(self):
        self.Q = [self.Qmin + (self.Qmax - self.Qmin) * np.random.uniform(0, 1) for _ in range(self.pop_size)]
    
    def __getPbest__(self):
        index_of_min_fitness = np.argmin(self.values['fitness'][-1])
        return list(zip(*self.values['pop'][-1]))[index_of_min_fitness]

    def execute(self):
        new_sol = [[0 for _ in range(self.pop_size)] for _ in range(len(self.bounds))]
        bats = list(zip(*self.bats))
        v = list(zip(*self.velocity))
        new_bats = list(zip(*new_sol))

        for _ in range(self.max_iter):
            self.values['pop'].append(self.bats)
            self.values['fitness'].append(self.function(self.bats))

            for i in range(len(bats)):
                self.__setFrequency__()

                v[i] += (np.array(bats[i]) - np.array(self.__getPbest__())) * self.Q[i]
                
                new_bats[i] = bats[i] + v[i]
                
                if np.random.random_sample() > self.r:
                    new_bats[i] = np.array(self.__getPbest__()) + 0.001 * rnd.gauss(0, 1)
                
                Fnew = self.function(new_bats[i])
                if (Fnew <= self.values['fitness'][-1][i]) and (np.random.random_sample() < self.A):
                    bats[i] = new_bats[i]
                    self.values['fitness'][-1][i] = Fnew







from functions import *

if __name__ == '__main__':
    #test = bao(rastrigin, pop_size=50, bounds=[[-5.12, 5.12]]*20, A=0.7, r=0.1, Qmin=-0.5, Qmax=0.5, max_iter=500)
    test = bao(mishras_bird, pop_size=100, bounds=[[-10, 0], [-6.5, 0]], A=0.7, r=0.1, Qmin=-0.6, Qmax=0.6, max_iter=300)
    
    test.execute()
    print(min(test.values['fitness'][-1]))