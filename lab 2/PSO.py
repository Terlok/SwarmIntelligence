import numpy as np
from functions import *

class ParticleOptimization:
    def __init__(self, particles:int=20, bounds:list= None, hyper_parameters:list=[0.1, 0.1, 0.8], function:str=None, max_iter:int=100) -> None:
        self.size = particles
        self.bounds = bounds
        # First for particles. Second for population. Last for speed.
        self.hyper_parameters = hyper_parameters
        self.function = function
        self.max_iter = max_iter
        self.values = {'X':[], 'pbest': [], 'pbest_obj': []}

    def __create_vector__(self) -> list:
        points = []
        for i in range(len(self.bounds)):
            points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) for _ in range(self.size)])
        return np.array(points)

    def process_particles(self) -> None:
        X = self.__create_vector__()
        V = np.random.randn(len(self.bounds), self.size) * 0.1

        c1, c2, w = self.hyper_parameters
        pbest = X
        pbest_obj = self.function(X)
        gbest = pbest[:, pbest_obj.argmin()]
        gbest_obj = pbest_obj.min()

        for _ in range(self.max_iter):
            r1, r2 = np.random.rand(2)
            V = w * V + c1*r1*(pbest - X) + c2*r2*(gbest.reshape(-1,1)-X)
            X = X + V
            obj = self.function(X)
            pbest[:, (pbest_obj >= obj)] = X[:, (pbest_obj >= obj)]
            pbest_obj = np.minimum(pbest_obj, obj)
            gbest = pbest[:, pbest_obj.argmin()]
            gbest_obj = pbest_obj.min()
            self.values['X'].append(X)
            self.values['pbest'].append(pbest)
            self.values['pbest_obj'].append(pbest_obj)
            
        return gbest, gbest_obj

        

from graphics import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# if __name__ == '__main__':
    # print(pso.values['X'])
    # print(pso.values['X'][:-1])
    # print(pso.values['pbest'])
    # print(pso.values['pbest_obj'][0])

    # x = np.linspace(-1.5, 1.5, 100)
    # y = np.linspace(-1.5, 1.5, 100)
    # X, Y = np.meshgrid(x, y)
    # Z = rosenbrock1(X, Y)

    # # Create a 3D plot of the Rastrigin function
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # #ax.plot_surface(X, Y, Z, cmap='viridis')
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')

    # # Plot the solution found by the PSO algorithm
    
    
    # ax.scatter([i[0] for i in pso.values['X']], [i[1] for i in pso.values['X']], pso.values['pbest_obj'], color='red')
    # plt.show()
    
    # create_folders()
    # anim = Animation('rosenbrock1', pso.interval, rosenbrock1, pso.values)
    # anim.animate()
