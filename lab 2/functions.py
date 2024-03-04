import numpy as np

def rastrigin(X):
    A = 10
    n = len(X)
    result = 0
    for xi in X:
        result += xi**2 - A * np.cos(2 * np.pi * xi)
    return A * n + result
    
def rosenbrock1(X):
    x = np.array(X[0])
    y = np.array(X[1])
    condition_1 = ( (x - 1)**3 - y + 1 >= 0 )
    condition_2 = ( x + y - 2 >= 0 )

    func_values = np.array((1-x)**2 + 100*(y-x**2)**2)
    func_values[np.logical_and(condition_1, condition_2)] = 10000
    return func_values

def rosenbrock2(X):
    x = np.array(X[0])
    y = np.array(X[1])
    condition = ( x**2 + y**2 >= 2 )
    
    func_values = np.array((1-x)**2 + 100*(y-x**2)**2)
    func_values[condition] = 10000
    return func_values

def mishras_bird(X):
    x = np.array(X[0])
    y = np.array(X[1])
    condition = ( (x + 5)**2 + (y - 5)**2 >= 25 )

    func_values = np.exp((1-np.cos(x))**2)*np.sin(y) + np.exp((1-np.sin(y))**2)*np.cos(x) + (x-y)**2
    
    func_values = np.array(func_values)  # Convert func_values to a numpy array
    func_values[condition] = 10000
    return func_values

def simionescu(X):
    x = X[0]
    y = X[1]
    condition = ( x**2 + y**2 >= (1 + 0.2*np.cos(8 * np.arctan(np.divide(x, y))))**2 )

    func_values = 0.1*x*y
    func_values = np.array(func_values)  # Convert func_values to a numpy array
    func_values[condition] = 10000
    return func_values

def reducer_weight(X):
    pass

def spring_weights():
    pass

def test_func(X):
    x = X[0]
    y = X[1]
    return (x-3.14)**2 + (y-2.72)**2 + np.sin(3*x+1.41) + np.sin(4*y-1.73)