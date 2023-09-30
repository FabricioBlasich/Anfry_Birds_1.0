""" Cosas a tener en cuenta, supongamos que la siguiente es la panatalla,
    en pygame, (0, 0) del eje x,y se ubica en la esquina superior izquierda
    de la pantalla 
"""
# ______________________________________________________________
#|######################################################
#|(0,0)                                                #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|                                                     #
#|######################################################
# 



###################### Librerias ######################
import pygame
import os  #os = sistema operativo, para ayudar a encontrar el camino a las imagenes
import numpy as np
import math
import time
import random
from decimal import Decimal, getcontext


###################### Variables Globales ######################
TOLERANCIA = 1e-6
MAX_ITER = 1000
EST_INICIAL = 450  #(WIDTH/2) #Metodo de Newton, PuntoFijo
WIDTH  = 1200
HEIGHT = 650
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 10  #Fotogramas por segundo
RED_BIRD = pygame.image.load("C:/Users/fabri/OneDrive/Escritorio/Metodos_Numericos/Presentacion/angry-birds-python/resources/images/red-bird3.png").convert_alpha()
GREEN_BIRD = pygame.transform.scale(pygame.image.load("C:/Users/fabri/OneDrive/Escritorio/Metodos_Numericos/AngryBirds1.0/images/pig_failed.png").convert_alpha(), (55,55))
BACKGROUND= pygame.transform.scale(pygame.image.load("C:/Users/fabri/OneDrive/Escritorio/Metodos_Numericos/AngryBirds1.0/images/background.png").convert_alpha() ,(WIDTH, HEIGHT))
START_X = 0
GROUND = screen.get_height() - 50
GRAVEDAD = 9.80665
x = []  # Lista donde almacenare la posicion en x del angry bird
y = []  # Lista donde almacenare la posicion en y del angry bird
getcontext().prec = 28 #Presicion de los numeros flotantes para calcular los tiempos



###################### Funcion Main ######################
def main():
    red_bird = pygame.Rect(START_X, GROUND, 5, 5)  #Asocio un rectangulo a la imagen png del angty bird, para facilitar la variacion de su posicion en pantalla
    green_bird = pygame.Rect(random.randint(300,1000), GROUND, 50, 50)
    fuente = pygame.font.Font(None, 50)
    vo = 100 #Velocidad inicial
    theta = 45 #Angulo inicial
    clock = pygame.time.Clock()
    shoot = False #Esta variable nos permitira controlar cuando el pajaro es lanzado
    running  = True #Esta variable nos permite ejecutar el programa, cambiara a False cuando el usuraio presione el boton X de arriba a la derecha d ela pantalla
    metodo = 1
    puntaje = 0
    texto_puntaje = fuente.render(f'Puntaje: {puntaje}', True, (0, 0, 0))
    method = "Biseccion"
    load_music()
    while running :
        clock.tick(FPS) #Controla la velocidad del bucle While (este se ejecutara 60 veces por segudo)
        
        for event in pygame.event.get():           #En este bucle se controla si el usuario
            if event.type == pygame.QUIT:          #presiona o no X para terminar el programa
                running  = False

        pygame.display.set_caption("Angulo" + str(theta) + "  Velocidad:" + str(vo) + "  Metodo: " + method)   #Permite visualizar al usuario la velocidad y angulo con el que sera lanzado el angry bird
        draw_screen(red_bird,green_bird,texto_puntaje) #Esta funcion actualiza la posicon del angry bird en pantalla

        keys_pressed = pygame.key.get_pressed() #Esta funcion nos devuelve una lista que contiene las teclas presionadas por el usuario
        if keys_pressed[pygame.K_SPACE]:   #Si el usuario presiona la tecla espacio el angry bird sera disparado
            shoot = True
            draw_trajectory(vo, theta, x, y, metodo)  #Esta funcion calcula y llena las listas x e y que contienen la posicion del angry bird en pantalla
            while shoot == True:
                clock.tick(60)    #Controla la velocidad del bucle While (este se ejecutara 60 veces por segudo)
                if (len(x)>0 and len(y) > 0):  
                    red_bird.x = x.pop(0)     
                    red_bird.y = HEIGHT - y.pop(0)
                    if red_bird.y < GROUND:
                        draw_screen(red_bird,green_bird,texto_puntaje)
                else:
                    shoot = False
                    red_bird.x = START_X
                    red_bird.y = GROUND
                if red_bird.colliderect(green_bird):
                    green_bird.x = random.randint(300,1000)
                    puntaje += 1
                    texto_puntaje = fuente.render(f'Puntaje: {puntaje}', True, (0, 0, 0))
                    

        #Con el siguiente conjunto de if permiten variar y controlar la velocidad y angulo de tiro 
        if keys_pressed[pygame.K_UP] and theta < 90: 
            theta += 1
        if keys_pressed[pygame.K_DOWN] and theta >= 10:
            theta -= 1
        if keys_pressed[pygame.K_RIGHT] and vo < 125:
            vo += 1
        if keys_pressed[pygame.K_LEFT] and vo > 25:
            vo -= 1
        if keys_pressed[pygame.K_p]:
            if metodo == 5:
                metodo = 1
            else:
                metodo += 1
            
            if metodo == 1:
                method = "Biseccion"
            elif metodo == 2:
                method = "Newton_raphson"
            elif metodo == 3:
                method = "Punto Fijo"
            elif method == 4:
                method = "Regula Falsi"
            else:
                method = "Secante"





###################### Funciones ######################

def f(vo, theta, t): #Esta funcion describe la altura del angry bird en funcion del tiempo
    return vo*np.sin(theta)*t - 0.5*GRAVEDAD*(t**2)  #Considero y0 = 0


def df(vo, theta, t):  #Derivada de la funcion que describe la altura del angry bird en funcion del tiempo
    return vo*np.sin(theta) - GRAVEDAD*t


def fIteracion(vo, theta, t):           #Funcion que se usa en el metodo Punto fijo
    return ((vo*np.sin(theta)*t)/(0.5*GRAVEDAD))**(1/2)


def draw_screen(red_bird,green_bird,puntaje):  #Esta funcion actualiza la posicon del angry bird en pantalla
    screen.blit(BACKGROUND, (0,0))
    screen.blit(RED_BIRD, (red_bird.x,red_bird.y))
    screen.blit(GREEN_BIRD,(green_bird.x,green_bird.y))
    screen.blit(puntaje, (START_X,0))
    pygame.display.update()






def draw_trajectory(vo, theta, x, y, metodo):
    theta = math.radians(theta)

    with open("C:/Users/fabri/OneDrive/Escritorio/Metodos_Numericos/AngryBirds1.0/src/tiempos.txt", 'r+') as archivo:
        contenido = archivo.read()  # Lee el contenido actual del archivo

        if metodo == 1:
            inicio = Decimal(time.time())
            tmax = biseccion(1,1000,vo,theta)
            fin = Decimal(time.time())
            archivo.write("Biseccion: " + str(fin-inicio) + "\n")
        elif metodo == 2:
            inicio = Decimal(time.time())
            tmax = newton_raphson(vo, theta)  #tiempo maximo de vuelo calculado con Newton_raphson
            fin = Decimal(time.time())
            archivo.write("Newton_raphson: " + str(fin-inicio) + "\n")
        elif metodo == 3:
            inicio = Decimal(time.time())
            tmax = puntoFijo(vo, theta)  #tiempo maximo de vuelo calculado con Newton_raphson
            fin = Decimal(time.time())
            archivo.write("Punto Fijo: " + str(fin-inicio) + "\n")
        elif metodo == 4:
            inicio = Decimal(time.time())
            tmax = regulaFalsi(1,1000,vo, theta)  #tiempo maximo de vuelo calculado con Newton_raphson
            fin = Decimal(time.time())
            archivo.write("Regula Falsi: " + str(fin-inicio) + "\n")
        elif metodo == 5:
            inicio = Decimal(time.time())
            tmax = secante(10,500,vo,theta)  #tiempo maximo de vuelo calculado con Newton_raphson
            fin = Decimal(time.time())
            archivo.write("Secante: " + str(fin-inicio) + "\n")
        
        archivo.close()

    intervalo_tiempos = np.arange(0, tmax, 0.1)  #frange me devuelve una lista que contiene un tiempos desde 0 a tmax, sobre el cual iterare y le dare valores a las funciones que describen la posicion x e t del angry bird
    for t in intervalo_tiempos:
        x.append(vo*np.cos(theta)*t)
        y.append(vo*np.sin(theta)*t - 0.5*GRAVEDAD*(t**2))


def load_music():
    song1 = 'C:/Users/fabri/OneDrive/Escritorio/Metodos_Numericos/AngryBirds1.0/sound/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


def newton_raphson(vo, theta):  #Uso el metodo de Newton para encontrar el 0
    x = EST_INICIAL             #de la funcion que describe la altula del angry bird en funcion del tiempo
    for i in range(MAX_ITER):   #dandonos asi tmax (tiempo de vuelo maximo)
        x_new = x - f(vo, theta, x) / df(vo, theta, x)
        if abs(x_new - x) < TOLERANCIA:
            return x_new
        x = x_new
    raise Exception("El método de Newton-Raphson no convergió")


def biseccion(a,b,vo,theta):
  i = 1
  p = (a + b)/2
  while(np.abs(f(vo,theta,p))>TOLERANCIA and i<=MAX_ITER):
    i += 1
    if(f(vo,theta,a)*f(vo,theta,p) > 0):
      a = p
    else:
      b = p
    p = (a + b)/2
  if(i > MAX_ITER):
    raise Exception("No se encontro la raiz")
  else:
    return p
  

def puntoFijo(vo,theta):
    x = EST_INICIAL
    for i in range(0,MAX_ITER):
        x_next = fIteracion(vo,theta, x)
        if abs(x_next-x)<TOLERANCIA:
            return x_next
        x = x_next
    raise ValueError("El método de Newton-Raphson no convergió")
    

def regulaFalsi(a,b,vo, theta):
    x = b-f(vo,theta,b)*(b-a)/(f(vo,theta,b)-f(vo,theta,a))
    iter = 1

    while iter<MAX_ITER and abs(f(vo,theta,x))>TOLERANCIA:
        iter += 1
        if f(vo,theta,a)*f(vo,theta,x)>0:
            a = x
        else:
            b = x
        x = b-f(vo,theta,b)*(b-a)/(f(vo,theta,b)-f(vo,theta,a))
        
    return x


def secante(a,b,vo,theta):
    x0 = a
    x1 = b
    for i in range(0,MAX_ITER):
        f0 = f(vo,theta,x0)
        f1 = f(vo,theta,x1)  
        # Evitar la división por cero
        if f1 - f0 == 0:
            raise ValueError("División por cero. Cambia los puntos iniciales.")
        # Calcula la próxima aproximación
        x_next = x1-f1*(x1-x0)/(f1-f0)
        # Comprueba la convergencia
        if abs(x_next - x1) < TOLERANCIA:
            return x_next
        # Actualiza los puntos iniciales para la siguiente iteración
        x0, x1 = x1, x_next

    raise Exception("El método de la Secante no convergió")


######################################################################################
pygame.init()

if __name__ == "__main__":
    main()

pygame.quit()