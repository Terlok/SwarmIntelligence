import numpy as np

def Var01(x, b1, b2):
    return b1 * (1 - np.exp(-b2 * x))

def Var11(x, b1, b2):
    return (b1 * b2) / (1 + b2*x)

def Var16(x, b1, b2, b3):
    return (b1 / b2) * np.exp(-0.5 * ((x-b3)/b2)**2)