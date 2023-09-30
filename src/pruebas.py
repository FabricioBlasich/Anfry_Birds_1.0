import numpy as np
import math
import matplotlib.pyplot as plt

GRAVEDAD = 9.80665


def f(t, vo=60, theta=math.radians(45)):
    return vo*np.sin(theta)*t - 0.5*GRAVEDAD*(t**2)  #Considero yo = 0


def df(vo, theta, t):
    return vo*np.sin(theta) - GRAVEDAD*t


def fIteracion(t, vo=60, theta=math.radians(45)):
   return ((vo*np.sin(theta)*t)/(0.5*GRAVEDAD))**(1/2)
   

def newton_raphson(initial_guess, tol=1e-6, max_iter=1000):
    x = initial_guess
    for i in range(max_iter):
        x_new = x - f(x) / df(60, math.radians(45), x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise Exception("El método de Newton-Raphson no convergió")

def biseccion(a, b, tol=1e-6, max_iter=1000):
  i = 1
  p = (a + b)/2
  while(np.abs(f(p)) > tol and i<=max_iter):
    i += 1
    if(f(a)*f(p) > 0):
      a = p
    else:
      b = p
    p = (a + b)/2
  if(i > max_iter):
    raise Exception("No se encontro la raiz")
  else:
    return p
  

def puntoFijo(x0,tol=1e-6, max_iter=1000):
    x = x0
    for i in range(0,max_iter):
        x_next = fIteracion(x)
        if abs(x_next-x)<tol:
            return x_next
        x = x_next
    raise ValueError("El método de Newton-Raphson no convergió")


def regulaFalsi(a,b,tol=1e-6, max_iter=1000):
    x = b-f(b)*(b-a)/(f(b)-f(a))
    iter = 1

    while iter<max_iter and abs(f(x))>tol:
        iter += 1
        if f(a)*f(x)>0:
            a = x
        else:
            b = x
        x = b-f(b)*(b-a)/(f(b)-f(a))
        
    return x

def secante(a,b,tol=1e-6, max_iter=1000):
    x0= a
    x1 = b
    for i in range(0,max_iter):
        f0 = f(x0)
        f1 = f(x1)  
        # Evitar la división por cero
        if f1 - f0 == 0:
            raise ValueError("División por cero. Cambia los puntos iniciales.")
        # Calcula la próxima aproximación
        x_next = x1 - f1 * (x1 - x0) / (f1 - f0)
        # Comprueba la convergencia
        if abs(x_next - x1) < tol:
            return x_next
        # Actualiza los puntos iniciales para la siguiente iteración
        x0, x1 = x1, x_next

    raise Exception("El método de la Secante no convergió")


x = np.linspace(-5,10,5)
plt.plot(x,f(x))
plt.title("Graficas")
plt.xlabel('x')
plt.ylabel('y')
#plt.show()
print(newton_raphson(100))
print(newton_raphson(100)*60*np.cos(math.radians(45)))
print(biseccion(5,10))
print(puntoFijo(100))
print(regulaFalsi(5,10))
print(str(secante(5,10)) + "---")


