import pygame
from pygame.math import Vector2
import random
from assets.color.colores import VERDE_CLARO
from assets.config.screen import cell_n, cell_size, screen

pygame.mixer.init()

sonido_manzana = pygame.mixer.Sound("assets/sounds/SnakeEatVoice.ogg")
sonido_choque =  pygame.mixer.Sound("assets/sounds/HeadBang.ogg")


class Serpiente:
    '''
    Clase para representar a la serpiente.

    :atributos:
        cuerpo(list): Lista contenedora de la posicion e inicio del lugar de la serpiente.
        direccion: Direccion en la que irá la serpiente inicialmente.
    '''
    def __init__(self):
        '''
        Constuctor: Inicializa la serpiente en posicion,lugar y direccion inicial (Mediante Vector2)

        Serpiente inicia en la posicion (5,10) y (6,10).
        Comienza con un largo de 2 (Entre mas vectores, mas segmentos inciales.), 
        '''
        self.cuerpo = [Vector2(6,10), Vector2(5,10)] #Cuerpo inicial de la serpiente.
        self.direccion = Vector2(1,0) #Direccion por defecto.


    def d_serpiente(self):
        '''
        Dibujo de la serpiente.

        Recorremos cada segmento(cuadro) del cuerpo(self.cuerpo),
        para luego dibujar cada uno en las coordenadas indicadas de cada uno.
        '''

        for cuadro in self.cuerpo:
            block_rect = pygame.Rect((cuadro.x * cell_size),(cuadro.y * cell_size), cell_size, cell_size) #.Rect almacena coordenadas rectangulares.
            pygame.draw.rect(screen,VERDE_CLARO, block_rect) #Dibujamos los rectangulos en la pantalla.
    
    def movimiento(self):
        """
        Movilidad de la serpiente.

        Simulamos el movimiento de la serpiente agregando un segmento en la posición de la cabeza,
        y eliminando el último segmento del cuerpo,
        se modifica el atributo cuerpo para realizar dicha acción.
        """

        cuerpo_mov = self.cuerpo[:-1] #Copia del cuerpo sin la cola.
        cuerpo_mov.insert(0,cuerpo_mov[0] + self.direccion) #Insertamos la "nueva" cabeza adelante de todo.
        self.cuerpo = cuerpo_mov[:] #Se actualiza la lista con el nuevo cuerpo.

    def crecer(self):
        # Al comer la fruta, agregamos un segmento al final de la lista.
        self.cuerpo.append(self.cuerpo[-1])


    def colision_cuerpo(self):
        '''
        Verifica la colision de la cabeza con algun segmento del cuerpo.

        :return:
            Tipo de dato bool.
            True: En caso de colisión con el cuerpo.
            False: Caso contrario.
        '''

        return self.cuerpo[0] in self.cuerpo[1:] #Compara si la cabeza esta en alguna posición del cuerpo.
    

    def colision_borde(self):
        '''
        Verifica si la cabeza toca algun borde del mapa.

        :return:
            Tipo de dato bool.
            True: En caso de tocar el borde del mapa.
            False: La cabeza sigue dentro del area del mapa.
        '''
        return not (0 <= self.cuerpo[0].x < cell_n and 0 <= self.cuerpo[0].y < cell_n)
    


class Fruta:
    '''
    Clase que representa la fruta.

    Inicia en una posicion random y luego se la dibuja en pantalla.
    '''
    def __init__(self):
        #Inicializa la fruta en una posicion aleatoria mediante el metodo spawn_random_fruta().
        self.spawn_random_fruta()
        #Sprite de la fruta a utilizar. Se la reescala al tamaño de la celda en el cual se encuentra la misma.
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/frutas/sprite_fruta.png').convert_alpha(), (cell_size, cell_size))


    def d_fruta(self):
        '''
        Dibuja la fruta en pantalla.

        Utilizamos el .Rect para crear un rectangulo,
        luego lo dibujamos en pantalla con el .draw.rect
        '''

        #Ubicacion de la fruta.
        spawn_fruta = pygame.Rect(self.posicion.x * cell_size, self.posicion.y * cell_size, cell_size, cell_size)
        #"Pegamos" el sprite de la fruta sobre la ubicación.
        screen.blit(self.sprite, spawn_fruta) 

    def spawn_random_fruta(self):
        '''
        Ubica la fruta en una posicion aleatoria dentro del area de juego.

        Utiliza coordenadas x,y provenientes del random.randint() para la ubicacion,
        dentro de la "grilla".
        '''
        self.x = random.randint(0,cell_n - 1) #Eje X
        self.y = random.randint(0,cell_n - 1) #Eje Y
        self.posicion = Vector2(self.x, self.y) #Posicion de la manzana (tupla)

class MainJuego:
    '''
    Clase principal del juego.

    Inicializamos el objeto Serpiente() y Fruta() para poder acceder a
    los metodos/funciones de las mismas.
    '''
    def __init__(self):
        #Instanciamos las clases Serpiente() y Fruta()
        self.snake = Serpiente()
        self.fruta = Fruta()
        self.puntuacion = 0 #Puntuacion de las manzanas.
        self.manzanas_comidas= 0 #Cantidad de manzanas ingeridas.

    def mov(self):
        '''
        Movimiento de la serpiente y colision.
        En caso de no colisionar con nada, podemos jugar.

        :return: bool
        '''
        self.snake.movimiento() #Movimiento de la serpiente.
        if self.colision(): #Si colisionamos/salimos de los limites, devuelve un booleano.
            return True


    def elementos(self):
        self.fruta.d_fruta() #Dibujamos la fruta en las coordenadas previstas.
        self.snake.d_serpiente() #Dibujamos la serpiente en las coordenadas iniciales indicadas.

    def colision(self):
        '''
        Verificamos si la serpiente chocó con su cuerpo, con un limite de mapa o si comió una manzana.
        Si .colision_borde() o .colision_cuerpo() son verdaderas, termina el juego,
        caso contrario, si la serpiente esta sobre la manzana(Comió), spawnea una nueva,
        extendemos la longitud de la serpiente mediante el metodo .crecer() y sumamos el puntaje.

        :returns: bool

        '''
        if self.snake.colision_borde() or self.snake.colision_cuerpo(): #Verificamos "colision".
            sonido_choque.play() #Sonido en caso de choque.
            print("¡Game Over!") #Test
            return True

        #Verificamos si la posicion de la cabeza de la serpiente está sobre una manzana.
        if self.fruta.posicion == self.snake.cuerpo[0]:
            self.fruta.spawn_random_fruta() #Spawn de la fruta.
            self.snake.crecer() #Aumento de longitud de la serpiente.
            #Suma el puntaje y aumenta con la cantidad de manzanas ingeridas.
            self.puntuacion += 3 + self.manzanas_comidas
            self.manzanas_comidas += 1 #Contador de manzanas aumenta.
            print(self.puntuacion)
            sonido_manzana.play() #Sonido de ingerir manzana.
            print("Comiendo!") #Test
        
