import numpy as np

class FireflyAlgorithm:
    def __init__(self, objective_function, n, bounds, max_iter=100, beta0=1.0, gamma=1.0):
        self.objective_function = objective_function
        self.n = n
        self.bounds = bounds
        self.max_iter = max_iter
        self.beta0 = beta0
        self.gamma = gamma
    
    def initialize_fireflies(self):
        return np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], (self.n, len(self.bounds)))
    
    def move_fireflies(self, fireflies, intensities):
        for i in range(self.n):
            for j in range(self.n):
                if intensities[i] > intensities[j]:
                    r = np.linalg.norm(fireflies[i] - fireflies[j])
                    beta = self.beta0 * np.exp(-self.gamma * r**2)
                    fireflies[i] += beta * (fireflies[j] - fireflies[i]) + 0.01 * np.random.randn(len(self.bounds))
                    fireflies[i] = np.clip(fireflies[i], self.bounds[:, 0], self.bounds[:, 1])
        intensities = [self.objective_function(firefly) for firefly in fireflies]
        return fireflies, intensities
    
    def optimize(self):
        fireflies = self.initialize_fireflies()
        intensities = [self.objective_function(firefly) for firefly in fireflies]
        
        for _ in range(self.max_iter):
            fireflies, intensities = self.move_fireflies(fireflies, intensities)
        
        best_index = np.argmin(intensities)
        best_solution = fireflies[best_index]
        best_fitness = intensities[best_index]
        
        return best_solution, best_fitness