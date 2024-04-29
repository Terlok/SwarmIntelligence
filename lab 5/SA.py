import math
import random as rnd
from knapsack import Knapsack

class SimulatedAnnealing:
    def __init__(self, knapsaskOBJ, initial_temperature, cooling_rate, num_iterations) -> None:
        self.capacity = knapsaskOBJ.capacity
        self.weights = knapsaskOBJ.values[0]
        self.profits = knapsaskOBJ.values[1]
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.iter = num_iterations
        self.num_items = len(self.weights)
        self.results = {'sol': [], 'fit': []}

    def evaluate(self, solution):
        total_weight = sum(solution[i] * self.weights[i] for i in range(self.num_items))
        total_value = sum(solution[i] * self.profits[i] for i in range(self.num_items))
        if total_weight > self.capacity:
            return -float('inf') 
        else:
            return total_value

    def simulated_annealing(self):
        current_solution = [rnd.choice([0, 1]) for _ in range(self.num_items)]
        current_fitness = self.evaluate(current_solution)
        self.results['sol'].append(current_solution)
        self.results['fit'].append(current_fitness)

        for _ in range(self.iter):
            neighbor_solution = current_solution.copy()
            index_to_flip = rnd.randint(0, self.num_items - 1)
            neighbor_solution[index_to_flip] = 1 - neighbor_solution[index_to_flip]
            neighbor_fitness = self.evaluate(neighbor_solution)

            if neighbor_fitness > current_fitness or rnd.random() < math.exp((neighbor_fitness - current_fitness) / self.temperature):
                current_solution = neighbor_solution
                current_fitness = neighbor_fitness

            if current_fitness > self.results['fit'][-1]:
                self.results['sol'].append(current_solution)
                self.results['fit'].append(current_fitness)

            self.temperature *= self.cooling_rate

        for i in range(len(self.results['fit'])):
            if self.results['fit'][i] == float('-inf'):
                self.results['fit'][i] = 0