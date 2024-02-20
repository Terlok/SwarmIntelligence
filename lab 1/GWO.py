import random as rnd
from functions import *
        
class GreyWolfOptimizer:
    def __init__(self, 
                 function:str, 
                 interval:list, 
                 step:float=0.1, 
                 epochs:int=50,
                 population_size:int=10,
                 dimensions:int=None
                 ) -> None:
        self.function = function
        self.interval = interval
        self.step = step
        self.epochs = epochs
        self.population_size = population_size
        self.dimensions = dimensions
        self.fit = {'population': [], 'fitness':[]}
        self.population = self.__create_population()
        self.min = None
        self.fittest_value = []
        self.best_iteration_values = []
    
    def optimize(self) -> None:
        for i in range(2*self.epochs):
            self.fit['population'].append(self.population)
            self.fit['fitness'].append(self.__fittest())

            self.fittest_value.append(self.__fittest_point(i)[0])
            self.population = self.__hunting(self.fittest_value[i])
        
        self.best_iteration_values = [self.function(*param) for param in self.fittest_value]
        self.min = self.__fittest_point(i)[1]
    
    def __hunting(self, fittest_value) -> list:
        new_pop = []
        for space in range(self.dimensions):
            space_pop = []
            for j in range(len(self.population[space])):
                space_pop.append(self.population[space][j] + self.step * (fittest_value[space] - self.population[space][j]) / self.__distance(fittest_value[space], self.population[space][j]))
            new_pop.append(space_pop)
        return new_pop

    def __create_population(self) -> list:
        self.interval = [self.interval] if type(self.interval[0]) == int else self.interval
        return [[rnd.uniform(*self.interval[i]) for _ in range(self.population_size)] for i in range(self.dimensions)]

    def __fittest(self) -> list:
        fitness = []
        for value in zip(*self.population):
            fitness.append(self.function(*value))
        return fitness

    def __fittest_point(self, epoch) -> tuple:
        min_fitness = min(self.fit['fitness'][epoch])
        min_index = [i for i, fitness in enumerate(self.fit['fitness'][epoch]) if fitness == min_fitness][0]
        return ([pop[min_index] for pop in self.fit['population'][epoch]], min_fitness)
    
    def __distance(self, a, b) -> float:
        return np.sqrt(a**2 + b**2)