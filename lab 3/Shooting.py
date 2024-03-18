import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
path = Path(__file__).parent.resolve()

def fun1(x, y, z, N, h, t):
    for k in range(N - 1):
        x[k + 1] = x[k] + h * z[k]
        y[k + 1] = y[k] + h * (y[k] ** 4 + x[k] ** 3 - 3 * np.sin(t[k] ** 2))
        if y[k + 1] < -5 or y[k + 1] > 5: 
            y[k + 1] = np.nan
        z[k + 1] = z[k] + h * (x[k] ** 2 + t[k] ** 2 - y[k] ** 2 * np.cos(z[k]))
    return x, y, z

def f1(X, N):
    return (X[N-1] - 2) ** 2

def fun2(x, y, z, N, h, t):
    for k in range(N - 1):
        y[k + 1] = y[k] + h * z[k]
        x[k + 1] = y[k] + h * (x[k]**2 - 5 * t[k]**2 + np.sin(x[k] * y[k] * t[k]))
        z[k + 1] = z[k] + h * (4 - 2 * np.cos(t[k] * (x[k]**2 - 5 * t[k]**2 + np.sin(x[k] * y[k] * t[k]))))
    return x, y, z

def f2(Y, N):
    return (Y[N-1] + 1) ** 2

class shooting:
    def __init__(self, filename, xa, xb, N, T, lb, ub):
        self.filename = filename
        self.xa = xa
        self.xb = xb
        self.N = N
        self.T = T
        self.lb = lb
        self.ub = ub
        self.h = np.divide((xb - xa), (N - 1))
        self.t = np.linspace(xa, xb, N)
        self.range = np.arange(lb, ub, 0.1)
        self.X = np.zeros(N)
        self.Y = np.zeros(N)
        self.Z = np.zeros(self.N)
        self.f = np.zeros_like(self.range)

    def execute(self):
        fig1 = plt.figure()
        for index, value in enumerate(self.range):
            self.Z[0] = value
            if self.T == 1:
                self.X, self.Y, self.Z = fun1(self.X, self.Y, self.Z, self.N, self.h, self.t)
                self.f[index] = f1(self.X, self.N)
            else:
                self.X, self.Y, self.Z = fun2(self.X, self.Y, self.Z, self.N, self.h, self.t)
                self.f[index] = f2(self.Y, self.N)
            plt.plot(self.X, self.Y, 'g')
            plt.axis([self.xa, self.xb, self.lb, self.ub])
            plt.xlabel(r'$x$')
            plt.ylabel(r'$y(\alpha$)')
            plt.title(r'$y(\alpha$)')
            plt.savefig(f'{path}\ShootingMethod\Y_{self.filename}.png')
        plt.close(fig1)

        fig2 = plt.figure()
        plt.plot(self.range, self.f)
        plt.xlabel(r'$\alpha$')
        plt.ylabel(r'$J(\alpha)$')
        plt.title(r'$J(\alpha)$')
        plt.savefig(f'{path}\ShootingMethod\J_{self.filename}.png')
        plt.close(fig2)
