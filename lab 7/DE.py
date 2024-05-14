import numpy as np

class DifferentialEvolution:
    def __init__(self, func, bounds, data, pop_size=50, mutation=0.8, crossover=0.7, max_iter=1000, tol=1e-6):
        self.func = func
        self.bounds = bounds
        self.data = data
        self.pop_size = pop_size
        self.mutation = mutation
        self.crossover = crossover
        self.max_iter = max_iter
        self.tol = tol
        self.param = {'fit': []}

    def optimize(self):
        pop = np.random.rand(self.pop_size, len(self.bounds))
        min_b, max_b = np.asarray(self.bounds).T
        diff = np.fabs(min_b - max_b)
        pop_denorm = min_b + pop * diff

        fitness = np.asarray([self.func(ind, *self.data) for ind in pop_denorm])
        best_idx = np.argmin(fitness)
        best_params = pop_denorm[best_idx]
        for _ in range(self.max_iter):
            for j in range(self.pop_size):
                idxs = [idx for idx in range(self.pop_size) if idx != j]
                a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + self.mutation * (b - c), 0, 1)
                cross_points = np.random.rand(len(self.bounds)) < self.crossover
                if not np.any(cross_points):
                    cross_points[np.random.randint(0, len(self.bounds))] = True
                trial = np.where(cross_points, mutant, pop[j])
                trial_denorm = min_b + trial * diff
                f = self.func(trial_denorm, *self.data)
                if f < fitness[j]:
                    fitness[j] = f
                    pop[j] = trial
                    if f < fitness[best_idx]:
                        best_idx = j
                        best_params = trial_denorm
            self.param['fit'].append(fitness.copy())
            if np.std(fitness) < self.tol:
                break
        best_fitness = self.func(best_params, *self.data)
        return best_params, best_fitness