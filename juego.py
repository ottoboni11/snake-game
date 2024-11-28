import pygame
from pygame.math import Vector2
from assets.sprites.backgrounds.background import background_image
from assets.color.colores import BLANCO
from assets.config.screen import screen
from assets.config.screen import fps
from funciones import dibujar_texto
from clases import MainJuego


def iniciar_juego():
    '''
    Funcion que contiene una breve configuracion de juego y el bucle de juego mismo.

    Incializa el reloj para poder controlar el temporizador del juego, gestiona el bucle principal
    del juego teniendo en cuenta los eventos realizados por el usuario dentro del juego,
    y actualizando elementos de este mismo, estado de juego, puntaje, estado de movimiento,
    longitud de la serpiente, posicion de la manzana.

    :returns: tuple Contiene el estado final del Menú y la puntuacion de partida.

    '''

    #Reloj del juego.
    tempo = pygame.time.Clock()

    #Variable que mantiene el bucle a no ser que cerremos el juego.
    corriendo = True

    #Actualizacion del movimiento de la serpiente.
    MOVIMIENTO_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(MOVIMIENTO_UPDATE,120)

    #Instanciamos el juego principal para poder utilizar sus metodos.
    main_juego = MainJuego()

    #Variable de control para evitar que la serpiente vuelva por donde venia.
    movimiento_previo = "RT"

    #Bucle principal del juego.
    while corriendo:

        #Bucle donde procesamos los eventos.
        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Click en cerrar actualiza la variable y cierra el bucle.
                corriendo = False #Variable actualizada.

            if event.type == MOVIMIENTO_UPDATE: #Movimiento.

                if main_juego.mov(): #Metodo .mov() corrobora si "colisionamos"
                    corriendo = False #Cierre de bucle, perdimos.
                    return ("menu final", main_juego.puntuacion)
                
            if event.type == pygame.KEYDOWN: 

                #Movimiento mediante las teclas pulsadas, se actualizan los vectores de direccion segun la tecla presionada. (Flechitas o WASD)
                if movimiento_previo != "DN" and (event.key == pygame.K_UP or event.key == pygame.K_w):
                    movimiento_previo = "UP"
                    main_juego.snake.direccion = Vector2(0,-1)
                if movimiento_previo != "UP" and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    movimiento_previo = "DN"
                    main_juego.snake.direccion = Vector2(0,1)
                if movimiento_previo != "LT" and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    movimiento_previo = "RT"
                    main_juego.snake.direccion = Vector2(1,0)
                if movimiento_previo != "RT" and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    movimiento_previo = "LT"
                    main_juego.snake.direccion = Vector2(-1,0)
        
        #Dibujo de los elementos de juego en la pantalla.
        screen.blit(background_image, (0, 0)) #Fondo de pantalla.
        main_juego.elementos() #Elementos de juego, serpiente y manzana.
        dibujar_texto(f"Puntaje:{main_juego.puntuacion}",20, 20,BLANCO ) #Puntaje del jugador.

        #Controlamos la velocidad maxima de juego.
        tempo.tick(fps)

        #Actualizacion de la pantalla.
        pygame.display.flip()
        