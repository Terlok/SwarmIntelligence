import numpy as np

class DifferentialEvolution:
    def __init__(self, bounds, x, y, pop_size=50, mutation=0.8, crossover=0.7, max_iter=1000, tol=1e-6):
        self.bounds = bounds
        self.x = x
        self.y = y
        self.pop_size = pop_size
        self.mutation = mutation
        self.crossover = crossover
        self.max_iter = max_iter
        self.tol = tol

    def func(self, x, b1, b2, b3):
        return (b1 / b2) * np.exp(-0.5 * ((x-b3)/b2)**2)
        #return b1 * (1 - np.exp(-b2 * x))

    def optimize(self):
        num_params = len(self.bounds)
        pop = np.random.rand(self.pop_size, num_params)
        min_b, max_b = np.asarray(self.bounds).T
        diff = np.fabs(min_b - max_b)
        pop_denorm = min_b + pop * diff

        fitness = np.asarray([np.mean((self.func(self.x, *ind) - self.y) ** 2) for ind in pop_denorm])
        best_idx = np.argmin(fitness)
        best_params = pop_denorm[best_idx]
        for i in range(self.max_iter):
            for j in range(self.pop_size):
                idxs = [idx for idx in range(self.pop_size) if idx != j]
                a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + self.mutation * (b - c), 0, 1)
                cross_points = np.random.rand(num_params) < self.crossover
                if not np.any(cross_points):
                    cross_points[np.random.randint(0, num_params)] = True
                trial = np.where(cross_points, mutant, pop[j])
                trial_denorm = min_b + trial * diff
                f = np.mean((self.func(self.x, *trial_denorm) - self.y) ** 2)
                if f < fitness[j]:
                    fitness[j] = f
                    pop[j] = trial
                    if f < fitness[best_idx]:
                        best_idx = j
                        best_params = trial_denorm
            if np.std(fitness) < self.tol:
                break
        best_fitness = np.mean((self.func(self.x, *best_params) - self.y) ** 2)
        return best_params, best_fitness