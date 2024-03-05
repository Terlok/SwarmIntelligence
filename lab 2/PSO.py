import numpy as np
from functions import reducer_weight

class ParticleOptimization:
    def __init__(self, particles:int=20, bounds:list= None, hyper_parameters:list=[0.1, 0.1, 0.8], function:str=None, max_iter:int=200) -> None:
        self.size = particles
        self.bounds = bounds
        # First for particles. Second for population. Last for speed.
        self.hyper_parameters = hyper_parameters
        self.function = function
        self.max_iter = max_iter
        self.values = {'pop':[], 'fitness': []}

    def __create_vector__(self) -> list:
        points = []
        if self.function != reducer_weight:
            for i in range(len(self.bounds)):
                points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) for _ in range(self.size)])
        else:
            for i in range(len(self.bounds)):
                points.append([np.random.uniform(self.bounds[i][0], self.bounds[i][1]) if j != 2 else int(np.random.uniform(self.bounds[i][0], self.bounds[i][1])) for j in range(self.size)])
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