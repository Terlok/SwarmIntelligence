import numpy as np

class FireflyAlgorithm:
    def __init__(self, function, colony_size, bounds, max_iter=100, beta0=1.0, gamma=1.0):
        self.function = function
        self.colony_size = colony_size
        self.bounds = bounds
        self.max_iter = max_iter
        self.beta0 = beta0
        self.gamma = gamma
        self.values = {'pop':[], 'fitness': []}
    
    def __create_vector__(self):
        points = []
        for i in range(len(self.bounds)):
            points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) for _ in range(self.colony_size)])
        return np.array(points)
    
    def move_fireflies(self, fireflies, intensities):
        for i in range(self.colony_size):
            for j in range(self.colony_size):
                if intensities[i] > intensities[j]:
                    r = np.linalg.norm(fireflies[:, i] - fireflies[:, j])
                    beta = self.beta0 * np.exp(-self.gamma * r**2)
                    fireflies[:, i] += beta * (fireflies[:, j] - fireflies[:, i]) + 0.01 * np.random.randn(len(self.bounds))
                    for k in range(len(self.bounds)):
                        fireflies[k, i] = np.clip(fireflies[k, i], self.bounds[k][0], self.bounds[k][1])
        intensities = [self.function(firefly) for firefly in fireflies.T]
        return fireflies, intensities
    
    def optimize(self):
        fireflies = self.__create_vector__()
        intensities = [self.function(firefly) for firefly in fireflies.T]
        
        for _ in range(self.max_iter):
            self.values['pop'].append(fireflies)
            self.values['fitness'].append(intensities)
            fireflies, intensities = self.move_fireflies(fireflies, intensities)
        
        best_index = np.argmin(intensities)
        best_solution = fireflies[:, best_index]
        best_fitness = intensities[best_index]
        
        return best_solution, best_fitness

from functions import *
import matplotlib.pyplot as plt

def scatter_plot(values):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    ax.scatter([i[0] for i in values['pop']], [i[1] for i in values['pop']], values['fitness'], color='red')
    plt.show()

if __name__ == '__main__':
    firefly1 = FireflyAlgorithm(rosenbrock1, colony_size=20, bounds=[[-1.5, 1.5], [-0.5, 2.5]])

    best_solution, best_fitness = firefly1.optimize()
    print(f'Best solution is: {best_solution}')
    print(f'Best fitness is: {best_fitness}')

    scatter_plot(firefly1.values)    