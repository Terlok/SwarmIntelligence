import numpy as np
import random as rnd

class bao:
    def __init__(self, function, pop_size, bounds, max_iter=200, A=0.5, r=0.5, Qmin=0.0, Qmax=1.0):
        self.function = function
        self.pop_size = pop_size
        self.bounds = bounds
        self.max_iter = max_iter
        self.A = A
        self.r = r
        self.Qmin = Qmin
        self.Qmax = Qmax

        self.bats = self.__init_population__()
        self.Q = np.zeros(self.pop_size)
        self.velocity = np.zeros((len(self.bounds), self.pop_size))

        self.best_solution = self.bats[:, 0]  # Початкове найкраще рішення
        self.best_fitness = float('inf')
        self.values = {'pop': [], 'fitness': []}

    def __init_population__(self):
        points = []
        for i in range(len(self.bounds)):
            points.append(np.random.uniform(self.bounds[i][0], self.bounds[i][1], self.pop_size))
        return np.array(points)

    def execute(self):
        for _ in range(self.max_iter):
            self.values['pop'].append(self.bats)
            fitness = self.function(self.bats)
            self.values['fitness'].append(fitness)

            for i in range(self.pop_size):
                self.Q[i] = self.Qmin + (self.Qmax - self.Qmin) * np.random.uniform()

                self.velocity[:, i] += (self.bats[:, i] - self.best_solution) * self.Q[i]

                new_bat = self.bats[:, i] + self.velocity[:, i]

                for j in range(len(self.bounds)):
                    new_bat[j] = np.clip(new_bat[j], self.bounds[j][0], self.bounds[j][1])

                if np.random.random() > self.r:
                    new_bat = self.best_solution + 0.001 * rnd.gauss(0, 1)

                new_fitness = self.function(new_bat)
                if new_fitness <= fitness[i] and np.random.random() < self.A:
                    self.bats[:, i] = new_bat
                    fitness[i] = new_fitness

                if new_fitness < self.best_fitness:
                    self.best_solution = new_bat
                    self.best_fitness = new_fitness