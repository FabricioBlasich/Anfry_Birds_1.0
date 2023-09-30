import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Definir las funciones a animar
def linear_function(x):
    return 14 - 5 * x

def quadratic_function(x):
    return x ** 2

# Crear valores de x en el rango de 0 a 5
x = np.linspace(0, 5, 100)
y_linear = linear_function(x)
y_quadratic = quadratic_function(x)

# Encontrar las intersecciones
intersections = np.argwhere(np.isclose(y_linear, y_quadratic, atol=0.05))

# Crear una figura y un eje
fig, ax = plt.subplots()
ax.set_xlim(0, 5)
ax.set_ylim(0, 15)  # Ajusta los límites en función de las funciones que estás animando

# Inicialización de la línea vertical
line_vertical, = ax.plot([], [], 'r--', lw=2, label='Intersection')

# Función de inicialización
def init():
    line_vertical.set_data([], [])
    return line_vertical,

# Función de animación
def animate(frame):
    if frame < len(intersections):
        x_data = [x[intersections[frame][0]]] * 2
        y_data = [0, 15]  # Ajusta la longitud de la línea vertical según tus necesidades
        line_vertical.set_data(x_data, y_data)
    else:
        line_vertical.set_data([], [])
    
    return line_vertical,

# Crear la animación
ani = FuncAnimation(fig, animate, init_func=init, frames=len(intersections) + 1, blit=True, interval=500)

# Mostrar la leyenda
ax.legend()

# Guardar la animación como un archivo HTML
ani.save('intersection_animation.html', writer='html')

# Mostrar la animación en el notebook
HTML('intersection_animation.html')