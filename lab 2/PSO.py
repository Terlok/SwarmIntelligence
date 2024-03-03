import numpy as np

class ParticleOptimization:
    def __init__(self, particles:int=20, bounds:list= None, hyper_parameters:list=[0.1, 0.1, 0.8], function:str=None, max_iter:int=100) -> None:
        self.size = particles
        self.bounds = bounds
        # First for particles. Second for population. Last for speed.
        self.hyper_parameters = hyper_parameters
        self.function = function
        self.max_iter = max_iter
        self.values = {'pop':[], 'fitness': []}

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
            self.values['pop'].append(X)
            self.values['fitness'].append(pbest_obj)

        return gbest, gbest_obj
    


from functions import *

if __name__ == '__main__':
    pso2 = ParticleOptimization(
                            particles=30,
                            max_iter=200,
                            bounds=[[-1.5, 1.5], [-1.5, 1.5]],
                            function=rosenbrock2,
                            )

    best_solution, best_fitness = pso2.process_particles()
    # anim = Animation('Rosenbrock1', pso2.bounds, Rosenbrock1, pso2.values)
    # anim.animate()

    print(f'Best solution is: {best_solution}')
    print(f'Best fitness is: {best_fitness}')

