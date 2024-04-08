import math
import random as rnd

def circle_point(radius, num_points):
    points = []
    theta = 2 * math.pi / num_points
    for i in range(num_points):
        x = radius * math.cos(i * theta)
        y = radius * math.sin(i * theta)
        points.append((x, y))
    return points

def random_points(x1, y1, x2, y2, point_count):
    return [(rnd.uniform(x1, y1), rnd.uniform(x2, y2)) for _ in range(point_count)]

def read_tsp_file(file_path):
    node_coords = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == "NODE_COORD_SECTION":
                break
        for line in file:
            if line.strip() == "EOF":
                break
            parts = line.strip().split()
            node_coords.append((float(parts[1]), float(parts[2])))
    return node_coords