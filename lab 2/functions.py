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
    
    func_values = np.array(func_values) 
    func_values[condition] = 10000
    return func_values

def simionescu(X):
    x = X[0]
    y = X[1]
    condition = ( x**2 + y**2 >= (1 + 0.2*np.cos(8 * np.arctan(np.divide(x, y))))**2 )

    func_values = 0.1*x*y
    func_values = np.array(func_values) 
    func_values[condition] = 10000
    return func_values

def reducer_weight(X):
    x1, x2, x3, x4, x5, x6, x7 = np.array(X)

    func_values = 0.7854*x1*x2**2*(3.3333*x3**2+14.9334*x3-43.0934) - 1.508*x1*(x6**2+x7**2)+7.4777*(x6**3+x7**3)+0.7854*(x4*x6**2+x5*x7**2)

    g1 = (np.divide(27, x1 * x2**2 * x3) - 1 > 0)
    g2 = (np.divide(397.5, x1 * x2**2 * x3**2) - 1 > 0)
    g3 = (np.divide(1.93 * x4**3, x2 * x3 * x6**4) - 1 > 0)
    g4 = (np.divide(1.93, x2 * x3 * x7**4) - 1 > 0)
    g5 = (np.divide(1, 110 * x6**3) * np.sqrt((np.divide(745 * x4, x2 * x3))**2 + 16.9 * 10**6) - 1 > 0)
    g6 = (np.divide(1, 85 * x7**3) * np.sqrt((np.divide(745 * x5, x2 * x3))**2 + 157.5 * 10**6) - 1 > 0)
    g7 = (np.divide(x2 * x3, 40) - 1 > 0)
    g8 = (np.divide(5*x2, x1) - 1 > 0)
    g9 = (np.divide(x1, 12 * x2) - 1 > 0)
    g10 = (np.divide(1.5 * x6 + 1.9, x4) - 1 > 0)
    g11 = (np.divide(1.1 * x7 + 1.9, x5) - 1 > 0)

    if g1 or g2 or g3 or g4 or g5 or g6 or g7 or g8 or g9 or g10 or g11:
        func_values = 10000
    return func_values

def spring_weights(X):
    x1, x2, x3 = np.array(X)
    func_values = (x3 + 2) * x2 * x1**2

    g1 = (1 - np.divide(x2**3 * x3, 7.178*x1**4) > 0)
    g2 = (np.divide(4*x2**2-x1*x2, 12.566*(x2*x1**3)-x1**4) + np.divide(1, 5.108*x1**2) - 1 >0),
    g3 = (1 - np.divide(140.45*x1, x2**2*x3) > 0),
    g4 = (np.divide(x1+x2, 1.5) - 1 > 0)

    if g1 or g2 or g3 or g4:
        func_values = 10000
    return func_values

def reducer_weight_pso(X):
    x1, x2, x3, x4, x5, x6, x7 = np.array(X)

    func_values = np.array(0.7854*x1*x2**2*(3.3333*x3**2+14.9334*x3-43.0934) - 1.508*x1*(x6**2+x7**2)+7.4777*(x6**3+x7**3)+0.7854*(x4*x6**2+x5*x7**2))

    conditions = [(np.divide(27, x1 * x2**2 * x3) - 1 > 0),
                (np.divide(397.5, x1 * x2**2 * x3**2) - 1 > 0),
                (np.divide(1.93 * x4**3, x2 * x3 * x6**4) - 1 > 0),
                (np.divide(1.93, x2 * x3 * x7**4) - 1 > 0),
                (np.divide(1, 110 * x6**3) * np.sqrt((np.divide(745 * x4, x2 * x3))**2 + 16.9 * 10**6) - 1 > 0),
                (np.divide(1, 85 * x7**3) * np.sqrt((np.divide(745 * x5, x2 * x3))**2 + 157.5 * 10**6) - 1 > 0),
                (np.divide(x2 * x3, 40) - 1 > 0),
                (np.divide(5*x2, x1) - 1 > 0),
                (np.divide(x1, 12 * x2) - 1 > 0),
                (np.divide(1.5 * x6 + 1.9, x4) - 1 > 0),
                (np.divide(1.1 * x7 + 1.9, x5) - 1 > 0)]

    if conditions:
        func_values = 10000
    return np.array(func_values)

def spring_weights_pso(X):
    x1, x2, x3 = np.array(X)
    func_values = (x3 + 2) * x2 * x1**2

    conditions = [(1 - np.divide(x2**3 * x3, 7.178*x1**4) > 0),
                (np.divide(4*x2**2-x1*x2, 12.566*(x2*x1**3)-x1**4) + np.divide(1, 5.108*x1**2) - 1 >0),
                (1 - np.divide(140.45*x1, x2**2*x3) > 0),
                (np.divide(x1+x2, 1.5) - 1 > 0)]

    if conditions:
        func_values = 10000
    return np.array(func_values)


def test_func(X):
    x = X[0]
    y = X[1]
    return (x-3.14)**2 + (y-2.72)**2 + np.sin(3*x+1.41) + np.sin(4*y-1.73)