import math
import random

class Edge:
    def __init__(self, x, y, weight, pheromone) -> None:
        self.x = x
        self.y = y
        self.weight = weight
        self.pheromone = pheromone

class Ant:
    def __init__(self, alpha, beta, len_data, edges) -> None:
        self.alpha = alpha
        self.beta = beta
        self.len_data = len_data
        self.edges = edges
        self.path = None
        self.distance = 0.0

    def _select_node(self):
        unvisited_nodes = [node for node in range(self.len_data) if node not in self.path]
        heuristic = sum([self.edges[self.path[-1]][node].weight for node in unvisited_nodes])
        roulette = sum([pow(self.edges[self.path[-1]][node].pheromone, self.alpha) * pow((heuristic / self.edges[self.path[-1]][node].weight), self.beta) for node in unvisited_nodes])
        wheel_pos = 0.0
        for node in unvisited_nodes:
            wheel_pos += pow(self.edges[self.path[-1]][node].pheromone, self.alpha) * pow((heuristic / self.edges[self.path[-1]][node].weight), self.beta)
            if wheel_pos >= random.uniform(0.0, roulette):
                return node

    def get_distance(self):
        self.distance = 0.0
        self.path = [random.randint(0, self.len_data - 1)]
        while len(self.path) < self.len_data:
            self.path.append(self._select_node())
        for i in range(self.len_data):
            self.distance += self.edges[self.path[i]][self.path[(i + 1) % self.len_data]].weight
        return self.distance
class ACO:
    def __init__(self, colony_size=10, min_scaling=0.001, alpha=1.0, beta=3.0,
                 rho=0.1, pheromone_coef=1.0, initial_pheromone=1.0, max_iter=100, data=None) -> None:
        self.colony_size = colony_size
        self.min_scaling = min_scaling
        self.rho = rho
        self.pheromone_coef = pheromone_coef
        self.max_iter = max_iter
        self.data = data
        self.len_data = len(data)
        self.labels = range(1, self.len_data + 1)
        self.edges = [[None] * self.len_data for _ in range(self.len_data)]
        for i in range(self.len_data):
            for j in range(i + 1, self.len_data):
                self.edges[i][j] = self.edges[j][i] = Edge(i, j, math.sqrt(pow(self.data[i][0] - self.data[j][0], 2.0) + pow(self.data[i][1] - self.data[j][1], 2.0)), initial_pheromone)
        self.ants = [Ant(alpha, beta, self.len_data, self.edges) for _ in range(self.colony_size)]
        self.values = {'points': [], 'best_path': [], 'distance': []}
        self.global_best_path = None
        self.global_best_distance = float('inf')

    def _add_pheromone(self, path, distance, weight=1.0):
        pheromone = self.pheromone_coef / distance
        for i in range(self.len_data):
            self.edges[path[i]][path[(i + 1) % self.len_data]].pheromone += weight * pheromone

    def max_min_method(self):
        for _ in range(self.max_iter):
            best_path = None
            best_distance = float('inf')
            for ant in self.ants:
                if ant.get_distance() < best_distance:
                    best_path = ant.path
                    best_distance = ant.distance
            if best_distance < self.global_best_distance:
                self.global_best_path = best_path
                self.global_best_distance = best_distance
            self._add_pheromone(self.global_best_path, self.global_best_distance)
            max_pheromone = self.pheromone_coef / self.global_best_distance
            min_pheromone = max_pheromone * self.min_scaling
            for i in range(self.len_data):
                for j in range(i + 1, self.len_data):
                    self.edges[i][j].pheromone *= (1.0 - self.rho)
                    if self.edges[i][j].pheromone > max_pheromone:
                        self.edges[i][j].pheromone = max_pheromone
                    elif self.edges[i][j].pheromone < min_pheromone:
                        self.edges[i][j].pheromone = min_pheromone
            self.values['points'].append(([self.data[i][0] for i in self.global_best_path], [self.data[i][1] for i in self.global_best_path]))
            self.values['best_path'].append(self.global_best_path)
            self.values['distance'].append(self.global_best_distance)