import numpy as np

def rastrigin(X):
    n = len(X)
    result = 0
    for xi in X:
        xi = np.array(xi)
        result += xi**2 - 10 * np.cos(2 * np.pi * xi)
    return 10 * n + result

def mishras_bird(X):
    x = np.array(X[0])
    y = np.array(X[1])
    condition = ( (x + 5)**2 + (y + 5)**2 >= 25 )

    func_values = np.exp((1-np.cos(x))**2)*np.sin(y) + np.exp((1-np.sin(y))**2)*np.cos(x) + (x-y)**2
    
    func_values = np.array(func_values) 
    func_values[condition] = 10000
    return func_values