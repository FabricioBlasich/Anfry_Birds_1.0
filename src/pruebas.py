import numpy as np
import math

GRAVEDAD = 9.80665


def f(vo, theta, t):
    return vo*np.sin(theta)*t - 0.5*GRAVEDAD*(t**2)  #Considero yo = 0

def df(vo, theta, t):
    return vo*np.sin(theta) - GRAVEDAD*t


def newton_raphson(initial_guess, tol=1e-6, max_iter=1000):
    x = initial_guess
    for i in range(max_iter):
        x_new = x - f(60, math.radians(45),x) / df(60, math.radians(45), x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise Exception("El método de Newton-Raphson no convergió")

print(newton_raphson(100))
print(newton_raphson(100)*60*np.cos(math.radians(45)))


