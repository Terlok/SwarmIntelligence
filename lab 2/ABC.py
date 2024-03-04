import numpy as np

class ABC:
    def __init__(self, function, bounds, colony_size=30, max_iter=200):
        self.function = function
        self.colony_size = colony_size
        self.bounds = bounds
        self.max_iter = max_iter
        self.n_employed_bees = int(self.colony_size / 2)
        self.n_onlooker_bees = self.n_employed_bees
        self.n_food_sources = self.n_employed_bees
        self.limit_scout = self.n_employed_bees * len(self.bounds)
        self.foodSources = self.__initializeFoodSources__()
        self.fitnesses = np.zeros(self.n_food_sources)
        self.trials = np.zeros(self.n_food_sources)
        self.values = {'pop': [], 'fitness': []}

    def getFitness(self, X):
        f = self.function(X)
        return 1 / (1 + f) if f >= 0 else 1 + abs(f)

    def __initializeFoodSources__(self):
        points = []
        for i in range(len(self.bounds)):
            points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) for _ in range(int(self.colony_size/2))])
        return np.array(points)

    def calculateFitnesses(self):
        for i in range(self.n_food_sources):
            self.fitnesses[i] = self.getFitness([self.foodSources[j][i] for j in range(len(self.bounds))])

    def performEmployedBeePhase(self):
        for i in range(self.n_employed_bees):
            new_soln = self.generateNewSolution(i)

            new_fitness = self.getFitness(new_soln)

            if new_fitness > self.fitnesses[i]:
                for j in range(len(self.bounds)):
                    self.foodSources[j][i] = new_soln[j]
                self.fitnesses[i] = new_fitness
                self.trials[i] = 0
            else:
                self.trials[i] += 1

    def performOnlookerBeePhase(self, prob_selection):
        i = 0
        j = 0

        while i < self.n_onlooker_bees:
            rnd = np.random.uniform(0, 1)
            if rnd <= prob_selection[j]:
                new_soln = self.generateNewSolution(j)
                new_fitness = self.getFitness(new_soln)
                if new_fitness > self.fitnesses[j]:
                    for dim in range(len(self.bounds)):
                        self.foodSources[dim][j] = new_soln[dim]
                    self.fitnesses[j] = new_fitness
                    self.trials[j] = 0
                else:
                    self.trials[j] += 1

                i += 1

            j = (j + 1) % self.n_food_sources

    def performScoutBeePhase(self):
        k = np.argmin(self.trials)
        if self.trials[k] <= self.limit_scout:
            return
        for dim in range(len(self.bounds)):
            self.foodSources[dim][k] = np.random.uniform(
                self.bounds[dim][0], self.bounds[dim][1])
        self.fitnesses[k] = self.getFitness([self.foodSources[dim][k] for dim in range(len(self.bounds))])

    def generateProbabilities(self):
        total_fitness = np.sum(self.fitnesses)
        return [fit / total_fitness for fit in self.fitnesses]

    def generateRandomInteger(self, low, high, dont_include):
        rnd = np.random.randint(low, high)
        return (
            self.generateRandomInteger(low, high, dont_include)
            if rnd == dont_include
            else rnd
        )

    def resetTrials(self):
        self.trials = np.zeros(self.n_employed_bees)

    def generateNewSolution(self, i):
        new_soln = []
        for j in range(len(self.bounds)):
            current = self.foodSources[j][i]

            partner = self.foodSources[j][
                self.generateRandomInteger(0, self.n_employed_bees, dont_include=i)
            ]

            new_val = current + np.random.uniform(-1, 1) * (current - partner)
            if new_val < self.bounds[j][0]:
                new_val = self.bounds[j][0]
            elif new_val > self.bounds[j][1]:
                new_val = self.bounds[j][1]

            new_soln.append(new_val)
        return new_soln

    def getCurrentBest(self):
        ind = np.argmax(self.fitnesses)
        return self.fitnesses[ind], [self.foodSources[i][ind] for i in range(len(self.bounds))]

    def optimize(self):
        self.calculateFitnesses()
        self.resetTrials()
        best_fitness, best_soln = self.getCurrentBest()

        for _ in range(self.max_iter):
            self.performEmployedBeePhase()
            prob_selection = self.generateProbabilities()
            self.performOnlookerBeePhase(prob_selection)
            temp_fitness, temp_soln = self.getCurrentBest()
            if temp_fitness > best_fitness:
                best_fitness = temp_fitness
                best_soln = temp_soln
            self.performScoutBeePhase()
            self.values['pop'].append(self.foodSources.copy())
            self.values['fitness'].append(self.fitnesses.copy())

        opt_val = self.function(best_soln)
        return best_soln, opt_val        