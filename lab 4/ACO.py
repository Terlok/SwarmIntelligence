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
        self.values = {'points': [], 'best_path': []}
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

    # def plot(self, name=None):
        # a=0
        # x = self.values['points'][a][0]
        # x.append(self.values['points'][a][0][0])
        # y = self.values['points'][a][1]
        # y.append(self.values['points'][a][1][0])
        # plt.plot(x, y, linewidth=1)
        # plt.scatter(x, y, s=math.pi * (math.sqrt(2.0) ** 2.0))
        # plt.title(f'Min_Max')
        # for i in self.values['best_path'][a]:
        #     plt.annotate(self.labels[i], self.data[i], size=8)
        
        # name = f'Min_Max.png'
        # plt.savefig(name, dpi=120)
        # plt.show()
        # plt.gcf().clear()

#     def plot(self, name=None):
#         fig, ax = plt.subplots(figsize=(8,6))

#         x = self.values['points'][-1][0]
#         x.append(self.values['points'][-1][0][0])
#         y = self.values['points'][-1][1]
#         y.append(self.values['points'][-1][1][0])

#         ax.plot(x, y, linewidth=1)
#         ax.scatter(x, y, s=math.pi * (math.sqrt(2.0) ** 2.0))
#         ax.set_title('Min_Max')

#         def animate(i):
#             ax.clear()
#             title = 'Iteration {:02d}'.format(i)
#             ax.set_title(title)
#             current_best_path = self.values['best_path'][i]  

#             for j in range(len(current_best_path) - 1):
#                 node1 = current_best_path[j]
#                 node2 = current_best_path[j + 1]
#                 ax.plot([self.data[node1][0], self.data[node2][0]], [self.data[node1][1], self.data[node2][1]], linewidth=1, color='b')
#                 ax.scatter(self.data[node1][0], self.data[node1][1], s=math.pi * (math.sqrt(2.0) ** 2.0), color='r')
#                 ax.annotate(self.labels[node1], self.data[node1], size=8)

#             last_node = current_best_path[-1]
#             first_node = current_best_path[0]
#             ax.plot([self.data[last_node][0], self.data[first_node][0]], [self.data[last_node][1], self.data[first_node][1]], linewidth=1, color='b')
#             ax.scatter(self.data[last_node][0], self.data[last_node][1], s=math.pi * (math.sqrt(2.0) ** 2.0), color='r')
#             ax.annotate(self.labels[last_node], self.data[last_node], size=8)

#             for node in range(len(self.data)):
#                 ax.annotate(self.labels[node], self.data[node], size=8)

#             return ax
        
#         anim = FuncAnimation(fig, animate, frames=range(self.max_iter), interval=200, blit=False, repeat=False)
#         anim.save(f'{path}Min_max.gif', dpi=120, writer='pillow')


# def generate_points_on_circle(radius, num_points):
#     points = []
#     theta = 2 * math.pi / num_points
#     for i in range(num_points):
#         x = radius * math.cos(i * theta)
#         y = radius * math.sin(i * theta)
#         points.append((x, y))
#     return points

    
# if __name__ == '__main__':
#     _colony_size = 5
#     #_data = [(random.uniform(-400, 400), random.uniform(-400, 400)) for _ in range(30)]
#     _data = generate_points_on_circle(1, 100)
#     max_min = SolveTSPUsingACO(colony_size=_colony_size, data=_data, max_iter=50)
#     max_min.max_min()
#     max_min.plot()