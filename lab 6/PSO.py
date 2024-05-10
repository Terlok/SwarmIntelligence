import numpy as np
from functions import *

class ParticleSwarmOptimization:
    def __init__(self, func, bounds, data, num_particles=50, max_iter=1000, tol=1e-6):
        self.func = func
        self.bounds = bounds
        self.x = np.array(data[0])
        self.y = np.array(data[1])
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.tol = tol
        self.param = {'fit': []}

    def optimize(self):
        min_bound, max_bound = np.asarray(self.bounds).T
        bounds_diff = np.fabs(min_bound - max_bound)

        particles = np.random.rand(self.num_particles, len(self.bounds)) * bounds_diff + min_bound
        velocities = np.zeros((self.num_particles, len(self.bounds)))
        best_particle_pos = particles.copy()
        best_swarm_pos = None
        best_swarm_val = np.inf

        for _ in range(self.max_iter):
            for j in range(self.num_particles):
                val = np.mean((self.func(self.x, *particles[j]) - self.y) ** 2)
                if val < best_swarm_val:
                    best_swarm_val = val
                    best_swarm_pos = particles[j].copy()
            r1, r2 = np.random.rand(2, len(self.bounds))
            velocities = velocities + (r1 * (best_particle_pos - particles) + r2 * (best_swarm_pos - particles))
            particles = particles + velocities
            particles = np.clip(particles, min_bound, max_bound)
            self.param['fit'].append([best_swarm_val])

            if np.std(best_particle_pos) < self.tol:
                break

        return best_swarm_pos, best_swarm_val