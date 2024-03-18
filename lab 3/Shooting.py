import numpy as np
import matplotlib.pyplot as plt

def fun1(x, y, z, N, h, t):
    for k in range(N - 1):
        x[k + 1] = x[k] + h * z[k]
        y[k + 1] = y[k] + h * (y[k] ** 4 + x[k] ** 3 - 3 * np.sin(t[k] ** 2))
        if y[k + 1] < -5 or y[k + 1] > 5: 
            y[k + 1] = np.nan
        z[k + 1] = z[k] + h * (x[k] ** 2 + t[k] ** 2 - y[k] ** 2 * np.cos(z[k]))
    return x, y, z

def fun2(x, y, z, N, h, t):
    pass

class shooting:
    def __init__(self, xa, xb, N):
        self.xa = xa
        self.xb = xb
        self.N = N

        self.h = np.divide((xb - xa), (N - 1))
        self.t = np.linspace(xa, xb, N)
        self.X = np.zeros(N)
        self.Y = np.zeros(N)
        self.Z = np.zeros(self.N)

    def execute(self):
        alpha_range = np.arange(-4, 4, 0.1)
        f = np.zeros_like(alpha_range)
        plt.figure()
        for alpha_index, alpha in enumerate(alpha_range):
            self.Z[0] = alpha
            
            self.X, self.Y, self.Z = fun1(self.X, self.Y, self.Z, self.N, self.h, self.t)
            
            plt.plot(self.X, self.Y, 'g')
            plt.grid(True)
            plt.axis([self.xa, self.xb, -5, 5])
            
            f[alpha_index] = (self.X[self.N-1] - 2) ** 2

        plt.show()


if __name__ == '__main__':
    shoot = shooting(xa=1, xb=3, N=5001)
    shoot.X[2] = 3
    shoot.Y[0] = 1
    shoot.execute()
    