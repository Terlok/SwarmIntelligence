import numpy as np

def rastrigin(x):
    n = len(x)
    return 10*n + sum([xi**2 - 10*np.cos(2*np.pi*xi) for xi in x])

def rosenbrock1(x, y):
    func_values = np.array((1-x)**2 + 100*(y-x**2)**2)
    condition_1 = (np.array(x) - 1)**3 - np.array(y) + 1 >= 0
    condition_2 = np.array(x) + np.array(y) - 2 >= 0

    func_values[np.logical_and(condition_1, condition_2)] = 10000
    return func_values

def rosenbrock2(x, y):
    condition = np.array(x)**2 + np.array(y)**2 >= 2
    
    func_values = np.array((1-x)**2 + 100*(y-x**2)**2)
    func_values[condition] = 10000
    return func_values

def matchishra_bird(x, y):
    return np.exp((1-np.cos(x))**2)*np.sin(y) + np.exp((1-np.sin(y))**2)*np.cos(x) + (x-y)**2

def simionescu(x, y):
    return 0.1*x*y

def reducer_weight():
    pass

def spring_weights():
    pass



def test_func(x,y):
    return (x-3.14)**2 + (y-2.72)**2 + np.sin(3*x+1.41) + np.sin(4*y-1.73)