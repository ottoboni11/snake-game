import pygame

#Dimensiones de la pantalla de juego.
cell_size = 32
cell_n = 25
screen = pygame.display.set_mode((cell_n * cell_size, cell_n * cell_size))

#Maximos frames por segundo.
fps = 60

# Dimensiones del menu
ANCHO = 800
ALTO = 800

# Sprite cabeza Snake.
icono = pygame.image.load("assets/sprites/snake/sprite_cabeza.png")
pygame.display.set_icon(icono)


# Botones del menú
boton_jugar = pygame.Rect(275, 250, 245, 60)
boton_ranking = pygame.Rect(275, 350, 245, 60)
boton_salir = pygame.Rect(275, 450, 245, 60)