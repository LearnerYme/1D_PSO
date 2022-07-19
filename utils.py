# 1D PSO algorithm
import numpy as np
import matplotlib.pyplot as plt

class args:
    def __init__(self, dt, c1, c2, omega, vmin, vmax, xmin, xmax) -> None:
        self.dt = dt
        self.c1 = c1
        self.c2 = c2
        self.omega = omega
        self.vmin = vmin
        self.vmax = vmax
        self.xmin = xmin
        self.xmax = xmax
        return

class particle:
    def __init__(self, conf:args, x: float = 0, v: float = 0) -> None:
        self.x = x
        self.v = v
        self.conf = conf
        self.fitness = 0
        self.best_x = 0
        self.best_x_group = 0
        self.best_fitness = -np.inf
        self.best_group = -np.inf
        return

    def update(self):
        # update velocity
        r1 = np.random.rand()
        r2 = np.random.rand()
        self.v = self.conf.omega * self.v + \
                    self.conf.c1 * r1 * (self.best_x - self.x) + \
                    self.conf.c2 * r2 * (self.best_x_group - self.x)

        # boudnary condition
        self.v = self.v if self.conf.vmin < self.v else self.conf.vmin
        self.v = self.v if self.conf.vmax > self.v else self.conf.vmax

        # update location
        self.x = self.x + self.conf.dt * self.v
        self.x = self.x if self.conf.xmin < self.x else self.conf.xmin
        self.x = self.x if self.conf.xmax > self.x else self.conf.xmax

        # calculate fitness function
        self.fitness = fitness.func(self)
        if self.fitness > self.best_fitness:
            self.best_x = self.x
            self.best_fitness = self.fitness
        return

class group:
    def __init__(self, n, conf:args, imax=1000) -> None:
        self.conf = conf
        self.particles = [
            particle(conf, 
                    np.random.uniform(conf.xmin, conf.xmax), 
                    np.random.uniform(conf.vmin, conf.vmax) 
            ) for _ in range(n)
        ]
        self.i = 0
        self.best_group = -np.inf
        self.best_x = 0
        self.imax = imax
        
        # plot
        self.fig, self.ax = plt.subplots(1, 1)

    def iteration(self):
        if self.i > self.imax:
            return
        self.i += 1
        for item in self.particles:
            item.update()
            if self.best_group < item.best_fitness:
                self.best_x = item.best_x
                self.best_group = item.best_fitness
        for item in self.particles: # this loop must be done after all the birds have updated their location
            item.best_group = self.best_group
            item.best_x_group = self.best_x
        return
        
    def info(self, detail=False):
        print('================================================')
        print(f'Iteration: {self.i} / {self.imax}')
        print(f'Best fitness: {self.best_group:.5f}, best location: {self.best_x:.3f}')
        if detail:
            for i, item in enumerate(self.particles):
                print(f'>Particle {i:5>}, velocity: {item.v:.3f}, location: {item.x:.3f}, fitness: {item.fitness:.3f}, best fitness: {item.best_fitness:.3f}')

    def draw(self, prefix='./'):
        self.ax.clear()
        x = np.linspace(self.conf.xmin, self.conf.xmax, 200)
        y = fitness.func_proto(x)
        self.ax.plot(x, y, 'k-')
        for item in self.particles:
            self.ax.plot(item.x, fitness.func(item), 'ro')
        self.ax.set_title(f'Iteration {self.i} of {self.imax}')
        self.fig.savefig(f'{prefix}/iter_{self.i}.png')
        return

class fitness:
    @classmethod
    def func(cls, p:particle):
        x = p.x
        return cls.func_proto(x)

    @staticmethod
    def func_proto(x):
        return x * np.sin(x) * np.cos(2*x) - 2 * x * np.sin(3*x)



        