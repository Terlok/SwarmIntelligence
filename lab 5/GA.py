import random as rnd
from knapsack import Knapsack

class GeneticAlgorithm:
    def __init__(self, knapsaskOBJ, number_of_bits, population_size, num_iterations) -> None:
        self.knapsaskOBJ = knapsaskOBJ
        self.w = number_of_bits
        self.pop_size = population_size
        self.iter = num_iterations
        self.pop = self.__create_population()
        self.results = {'pop': [], 'fit': []}

    def __create_population(self):
        return [''.join(map(str, [rnd.randint(0, 1) for _ in range(self.w)])) for _ in range(self.pop_size)]
    
    def __sort_by_fitness(self, pop):
        fitness = [self.knapsaskOBJ.fitness(i) for i in pop]
        pairs = zip(pop, fitness)
        sorted_pairs = sorted(pairs, key=lambda x: x[1])
        
        sorted_population = [pair[0] for pair in sorted_pairs]
        sorted_fitness = [pair[1] for pair in sorted_pairs]

        return sorted_population, sorted_fitness

    def produce_offspring(self):
        temp = self.pop.copy()
        offspring = []
        for _ in range(2 * self.pop_size):
            p1, p2 = rnd.sample(self.pop, 2)
            cross_point = rnd.randint(0, self.w-1)
            c1 = p1[:cross_point] + p2[cross_point:self.w] 
            c2 = p2[:cross_point] + p1[cross_point:self.w]
            
            offspring.append(self.__mutate(c1) if rnd.random() < 0.5 else self.__mutate(c2))
            
        temp.extend(offspring)
        fit = self.__sort_by_fitness(temp)
        
        self.pop = fit[0][len(fit[0])-self.pop_size:]
        fitness = fit[1][len(fit[0])-self.pop_size:]
        return self.pop, fitness

    def __mutate(self, gene):
        mutated_genotype = list(gene)
        repeating = 4 if rnd.random() < 0.5 else 2
        for _ in range(repeating):
            if rnd.random() < 0.7:
                random_gene_index = rnd.randint(0, len(gene) - 1)
                mutated_genotype[random_gene_index] = '0' if mutated_genotype[random_gene_index] == '1' else '1' 
        return ''.join(mutated_genotype)

    def genetic_optimization(self):
        for _ in range(self.iter):
            pop, fitness = self.produce_offspring()
            self.results['pop'].append(pop)
            self.results['fit'].append(fitness)
        print(self.results['pop'][-1])
        print(self.results['fit'][-1])