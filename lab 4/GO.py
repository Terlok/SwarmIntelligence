import math
import random
import numpy as np

class GO:
    def __init__(self, data, population_size, elite_size, mutation_rate=0.00001, generations=500):
        self.data = data
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.labels = range(1, len(data) + 1)
        self.values = {'points': [], 'best_path': [], 'distance': []}

    def distance(self, route):
        total_distance = 0
        for i in range(len(route)):
            from_point = self.data[route[i]]
            to_point = self.data[route[(i + 1) % len(route)]]
            total_distance += math.sqrt((to_point[0] - from_point[0]) ** 2 + (to_point[1] - from_point[1]) ** 2)
        return total_distance

    def initial_population(self):
        population = []
        for _ in range(self.population_size):
            population.append(random.sample(range(len(self.data)), len(self.data)))
        return population

    def tournament_selection(self, population, k=5):
        tournament = random.sample(population, k)
        return min(tournament, key=lambda x: self.distance(x))

    def breed(self, parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        gene1 = parent1[start:end]
        gene2 = [item for item in parent2 if item not in gene1]
        return gene1 + gene2

    def crossover(self, population):
        offspring = []
        for _ in range(self.population_size):
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            child = self.breed(parent1, parent2)
            offspring.append(child)
        return offspring

    def mutate(self, individual):
        for swapped in range(len(individual)):
            if random.random() < self.mutation_rate:
                swap_with = int(random.random() * len(individual))
                individual[swapped], individual[swap_with] = individual[swap_with], individual[swapped]
        return individual

    def mutate_population(self, population):
        mutated_population = []
        for individual in population:
            mutated_population.append(self.mutate(individual))
        return mutated_population

    def evolve(self, population):
        offspring = self.crossover(population)
        mutated_offspring = self.mutate_population(offspring)
        return mutated_offspring

    def optimize(self):
        population = self.initial_population()
        for _ in range(self.generations):
            population = self.evolve(population)
            population.sort(key=lambda x: self.distance(x))
            best_path = population[0]
            self.values['points'].append(([self.data[i][0] for i in best_path], [self.data[i][1] for i in best_path]))
            self.values['best_path'].append(population[0])
            self.values['distance'].append(self.distance(best_path))