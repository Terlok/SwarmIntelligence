import math
import random as rnd
from os import mkdir
from pathlib import Path

path = Path(__file__).parent.resolve()
datasets_path = f'{path}\\datasets'

def create_dataset_folder():
    Path(datasets_path).mkdir(parents=True, exist_ok=True)

class Knapsack:
    def __init__(self, capacity, d=None, weights_bound=None, profit_bound=None, input_data=0, exist=0, file_name=None) -> None:
        self.capacity = capacity
        self.d = d
        self.weights_bound = weights_bound
        self.profit_bound = profit_bound
        self.file_name = file_name
        self.exist = exist
        self.values = self.__parser() if input_data==0 else [weights_bound, profit_bound]

    def __generate_data(self):
        generated_weights = [rnd.randint(self.weights_bound[0], self.weights_bound[1]) for _ in range(self.d)]
        generated_profits = [rnd.randint(self.profit_bound[0], self.profit_bound[1]) for _ in range(self.d)]
        with open(f'{datasets_path}\\N_{self.d}_w_{self.weights_bound}_p_{self.profit_bound}.txt', 'w') as file:
            for i in zip(generated_weights, generated_profits):
                print(*i, file=file)
        self.file_name = f'{datasets_path}\\N_{self.d}_w_{self.weights_bound}_p_{self.profit_bound}.txt'

    def __parser(self):
        if self.exist != 1:
            self.__generate_data()
            with open(self.file_name, 'r') as file:
                return list(zip(*[map(int, item.strip().split()) for item in file.readlines()]))
        else:
            with open(f'{datasets_path}\\{self.file_name}', 'r') as file:
                return list(zip(*[map(int, item.strip().split()) for item in file.readlines()]))

    def __sum_function(self, param, indiviual):
        temp = 0
        for i, j in enumerate(indiviual):
            if i+1 > len(self.values[param]) and j == '1':
                temp += self.values[param][i % len(self.values[param])]
            elif i < len(self.values[param]) and j == '1':
                temp += self.values[param][i]
        return temp

    def fitness(self, indiviual):
        penalty = 0
        sumWeights = self.__sum_function(0, indiviual)
        if sumWeights > self.capacity:
            penalty = sumWeights + math.fabs(self.capacity - sumWeights)
        sumProfits = self.__sum_function(1, indiviual)
        fitness = sumProfits - penalty
        return fitness