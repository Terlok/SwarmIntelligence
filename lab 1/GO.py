import random as rnd
from functions import *
        
class GenotypeDecoder:
    def __init__(self, interval:list, population:list, number_of_bits:int, dimensions:int) -> None:
        self.interval = interval
        self.population = population
        self.w = number_of_bits
        self.dimensions = dimensions

    def bin_to_float(self) -> list: 
        self.interval = [self.interval] if type(self.interval[0]) == int else self.interval
        return [[(int(i, 2) / (2**self.w-1)) * (self.interval[j][1]-self.interval[j][0]) + self.interval[j][0] for i in self.population[j]] for j in range(self.dimensions)]
        
class Population:
    def __init__(self, function:str, interval:list, population_size:int, number_of_bits:int, dimensions:int) -> None:
        self.function = function
        self.interval = interval
        self.pop_size = population_size
        self.w = number_of_bits
        self.dimensions = dimensions
        self.population = self.__create_population()
        
    def __create_population(self) -> list:
        return [[''.join(map(str, [rnd.randint(0, 1) for _ in range(self.w)])) for _ in range(self.pop_size)]  for _ in range(self.dimensions)]
    
    def produce_offspring(self) -> int:
        for i in range(self.dimensions):
            offspring = []
            for _ in range(3 * self.pop_size):
                p1, p2 = rnd.sample(self.population[i], 2)
                cross_point = rnd.randint(0, self.w-1)
                c1 = p1[:cross_point] + p2[cross_point:self.w] 
                c2 = p2[:cross_point] + p1[cross_point:self.w]
                
                offspring.append(self.__mutate(c1) if rnd.random() < 0.5 else self.__mutate(c2))
            
            self.population[i].extend(offspring)

        fit = FitnessEvaluator(self.function, self.interval, self.population, self.w, self.dimensions).get_the_fittest()

        self.population = [sublist[:self.pop_size] for sublist in fit[0]]
        return self.population, fit[1][:self.pop_size]

    def __mutate(self, gene:str) -> str:
        mutated_genotype = list(gene)
        repeating = 2 if rnd.random() < 0.3 else 1
        for _ in range(repeating):
            if rnd.random() < 0.7:
                random_gene_index = rnd.randint(0, len(gene) - 1)
                mutated_genotype[random_gene_index] = '0' if mutated_genotype[random_gene_index] == '1' else '1' 
        return ''.join(mutated_genotype)

class FitnessEvaluator:
    def __init__(self, function:str, interval:list, population:list, number_of_bits:int, dimensions:int) -> None:
        self.function = function
        self.population = population
        self.dimensions = dimensions
        self.decoded_value_list = GenotypeDecoder(interval, population, number_of_bits, dimensions).bin_to_float()

    def get_the_fittest(self) -> list:
        return self.__sort_by_fitness()
        
    def __sort_by_fitness(self) -> list:
        if self.dimensions == 1:
            pairs = zip(self.population[0], [self.function(i) for i in self.decoded_value_list[0]])
            sorted_pairs = sorted(pairs, key=lambda x: x[1])
            
            sorted_population = [[pair[0] for pair in sorted_pairs]]
            sorted_function_value = [pair[1] for pair in sorted_pairs]
        else:
            a = [self.decoded_value_list[i] for i in range(self.dimensions)]
            decoded_pairs = list(zip(*a))
            b = [self.population[i] for i in range(self.dimensions)]
            population_pairs = list(zip(*b))
            pairs = zip(population_pairs, [self.function(*i) for i in decoded_pairs])
            
            sorted_pairs = sorted(pairs, key=lambda pair: pair[1])
            sorted_function_value = [pair[1] for pair in sorted_pairs]

            sorted_population = [[] for _ in range(self.dimensions)]
            for pair in sorted_pairs:
                for index, value in enumerate(pair[0]):
                    sorted_population[index].append(value)
        
        return sorted_population, sorted_function_value
    
class GeneticOptimizer:
    def __init__(self, 
                function:str,
                interval:list=None,
                population_size:int=10, 
                epochs:int=100,
                number_of_bits:int=16,
                dimensions:int = None,
                ) -> None:
        self.function = function
        self.interval = interval
        self.population_size = population_size
        self.epochs = epochs
        self.w = number_of_bits
        self.dimensions = dimensions
        self.fit = {'pop_value': [], 'fitness':[]}
        self.best_iteration_values = None
        self.min = None
    
    def optimize(self) -> None:
        population = Population(self.function, self.interval, self.population_size, self.w, self.dimensions)
        for _ in range(2*self.epochs):
            res = population.produce_offspring()
            self.fit['pop_value'].append(res[0])
            self.fit['fitness'].append(res[1])
        self.best_iteration_values = [min(i) for i in self.fit['fitness']]
        self.min = min(self.best_iteration_values)
