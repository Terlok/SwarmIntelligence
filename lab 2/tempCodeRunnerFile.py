    pso = ParticleOptimization(
                            particles=30,
                            iterations=50,
                            interval=[[-1.5, 1.5], [-1.5, 1.5]],
                            function=rosenbrock2,
                            )
    
    print(pso.process_particles())