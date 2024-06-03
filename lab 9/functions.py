import numpy as np

def Var01(x, b1, b2):
    return b1 * (1 - np.exp(-b2 * x))

def Var12(x, b1, b2, b3, b4):
    return b1 - b2*x - np.divide(1, np.pi) * np.arctan(np.divide(b3, x - b4))

def Var16(x, b1, b2, b3):
    return (b1 / b2) * np.exp(-0.5 * ((x-b3)/b2)**2)