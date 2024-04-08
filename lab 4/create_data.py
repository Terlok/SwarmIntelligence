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

def random_points(x1, x2, y1, y2, point_count):
    return [(rnd.uniform(x1, y1), rnd.uniform(x2, y2)) for _ in range(point_count)]