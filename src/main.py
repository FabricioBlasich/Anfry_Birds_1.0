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


###################### Variables Globales ######################
TOLERANCIA = 1e-6
MAX_ITER = 1000
EST_INICIAL = 450  #(WIDTH/2) #Metodo de Newton
WIDTH  = 1200
HEIGHT = 650
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60  #Fotogramas por segundo
RED_BIRD = pygame.image.load(os.path.join("AngryBirds1.0", "images", "red-bird.png"))
BACKGROUND= pygame.transform.scale(pygame.image.load(os.path.join("AngryBirds1.0", "images", "background.png")),(WIDTH, HEIGHT))
START_X = 0
GROUND = screen.get_height() - 75
GRAVEDAD = 9.80665
x = []  # Lista donde almacenare la posicion en x del angry bird
y = []  # Lista donde almacenare la posicion en y del angry bird



###################### Funcion Main ######################
def main():
    red_bird = pygame.Rect(START_X, GROUND, 5, 5)  #Asocio un rectangulo a la imagen png del angty bird, para facilitar la variacion de su posicion en pantalla
    vo = 100 #Velocidad inicial
    theta = 45 #Angulo inicial
    clock = pygame.time.Clock()
    shoot = False #Esta variable nos permitira controlar cuando el pajaro es lanzado
    running  = True #Esta variable nos permite ejecutar el programa, cambiara a False cuando el usuraio presione el boton X de arriba a la derecha d ela pantalla
    
    while running :
        clock.tick(FPS) #Controla la velocidad del bucle While (este se ejecutara 60 veces por segudo)
        
        for event in pygame.event.get():           #En este bucle se controla si el usuario
            if event.type == pygame.QUIT:          #presiona o no X para terminar el programa
                running  = False

        pygame.display.set_caption("Angulo" + str(theta) + "  Velocidad:" + str(vo))   #Permite visualizar al usuario la velocidad y angulo con el que sera lanzado el angry bird
        draw_screen(red_bird) #Esta funcion actualiza la posicon del angry bird en pantalla

        keys_pressed = pygame.key.get_pressed() #Esta funcion nos devuelve una lista que contiene las teclas presionadas por el usuario
        if keys_pressed[pygame.K_SPACE]:   #Si el usuario presiona la tecla espacio el angry bird sera disparado
            shoot = True
            draw_trajectory(vo, theta, x, y)  #Esta funcion calcula y llena las listas x e y que contienen la posicion del angry bird en pantalla
            while shoot == True:
                clock.tick(FPS)    #Controla la velocidad del bucle While (este se ejecutara 60 veces por segudo)
                if (len(x)>0 and len(y) > 0):  
                    red_bird.x = x.pop(0)     
                    red_bird.y = HEIGHT - y.pop(0)
                    if red_bird.y < GROUND:
                        draw_screen(red_bird)
                else:
                    shoot = False
                    red_bird.x = START_X
                    red_bird.y = GROUND

        #Con el siguiente conjunto de if permiten variar y controlar la velocidad y angulo de tiro 
        if keys_pressed[pygame.K_UP] and theta < 90: 
            theta += 1
        if keys_pressed[pygame.K_DOWN] and theta >= 10:
            theta -= 1
        if keys_pressed[pygame.K_RIGHT] and vo < 125:
            vo += 1
        if keys_pressed[pygame.K_LEFT] and vo > 25:
            vo -= 1



###################### Funciones ######################

def f(vo, theta, t): #Esta funcion describe la altura del angry bird en funcion del tiempo
    return vo*np.sin(theta)*t - 0.5*GRAVEDAD*(t**2)  #Considero y0 = 0


def df(vo, theta, t):  #Derivada de la funcion que describe la altura del angry bird en funcion del tiempo
    return vo*np.sin(theta) - GRAVEDAD*t


def draw_screen(red_bird):  #Esta funcion actualiza la posicon del angry bird en pantalla
    screen.blit(BACKGROUND, (0,0))
    screen.blit(RED_BIRD, (red_bird.x, red_bird.y))
    pygame.display.update()


def draw_trajectory(vo, theta, x, y):
    theta = math.radians(theta)

    tmax = newton_raphson(vo, theta)  #tiempo maximo de vuelo calculado con Newton_raphson

    intervalo_tiempos = np.arange(0, tmax, 0.1)  #frange me devuelve una lista que contiene un tiempos desde 0 a tmax, sobre el cual iterare y le dare valores a las funciones que describen la posicion x e t del angry bird
    for t in intervalo_tiempos:
        x.append(vo*np.cos(theta)*t)
        y.append(vo*np.sin(theta)*t - 0.5*GRAVEDAD*(t**2))


def newton_raphson(vo, theta):  #Uso el metodo de Newton para encontrar el 0
    x = EST_INICIAL             #de la funcion que describe la altula del angry bird en funcion del tiempo
    for i in range(MAX_ITER):   #dandonos asi tmax (tiempo de vuelo maximo)
        x_new = x - f(vo, theta, x) / df(vo, theta, x)
        if abs(x_new - x) < TOLERANCIA:
            return x_new
        x = x_new
    raise Exception("El método de Newton-Raphson no convergió")
    

######################################################################################
pygame.init()

if __name__ == "__main__":
    main()

pygame.quit()