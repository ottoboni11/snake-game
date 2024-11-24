import pygame,random
from pygame.math import Vector2

#VIBORA
class SERPIENTE:
    #Inicializamos la serpiente.
    def __init__(self):
        self.cuerpo = [Vector2(5,10), Vector2(6,10)]
        self.direccion = Vector2(1,0)

    #Dibujamos la forma de la serpiente.
    def spawn_serpiente(self):
        for cuadro in self.cuerpo:
            block_rect = pygame.Rect((cuadro.x * cell_size),(cuadro.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen,(100,100,100), block_rect)
    
    def movimiento(self):
        cuerpo_mov = self.cuerpo[:-1]
        cuerpo_mov.insert(0,cuerpo_mov[0] + self.direccion)
        self.cuerpo = cuerpo_mov[:]

    def crecer(self):
        # Al comer la fruta, agregamos un segmento más a la serpiente.
        self.cuerpo.append(self.cuerpo[-1])

    #Colision con el propio cuerpo, retorna un booleano.
    def colision_cuerpo(self):
        return self.cuerpo[0] in self.cuerpo[1:]
    
    #Colision con el borde, retorna un booleano.
    def colision_borde(self):
        # Verificamos si la cabeza de la serpiente toca los bordes del juego
        return not (0 <= self.cuerpo[0].x < cell_n and 0 <= self.cuerpo[0].y < cell_n)

#Fruta
class FRUTA:
    def __init__(self):
        #Inicializamos la serpiente.
        self.spawn_random_fruta()
    
    def d_fruta(self):
        #Dibujamos la fruta.
        spawn_fruta = pygame.Rect(self.posicion.x * cell_size, self.posicion.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen,(200,120,114),spawn_fruta)

    def spawn_random_fruta(self):
        self.x = random.randint(0,cell_n - 1)
        self.y = random.randint(0,cell_n - 1)
        self.posicion = Vector2(self.x, self.y)

class JUEGO:
    def __init__(self):
        #Creamos el objeto serpiente.
        self.snake = SERPIENTE()
        #Creamos el objeto fruta.
        self.fruta = FRUTA()

    def mov(self):
        self.snake.movimiento()
        if self.colision():
            return True


    def elementos(self):
        self.fruta.d_fruta()
        self.snake.spawn_serpiente()

    def colision(self):
        #Verificamos si colisionamos con un borde o el propio cuerpo.
        if self.snake.colision_borde() or self.snake.colision_cuerpo():
            print("¡Game Over!")
            return True
        #Verificamos si comio la manzana.
        if self.fruta.posicion == self.snake.cuerpo[0]:
            self.fruta.spawn_random_fruta()
            self.snake.crecer()
            print("Comiendo!")


#Inicializacion pygame.
pygame.init()
cell_size = 32
cell_n = 30
screen = pygame.display.set_mode((cell_n * cell_size, cell_n * cell_size))
tempo = pygame.time.Clock()
corriendo = True

MOVIMIENTO_UPDATE = pygame.USEREVENT
pygame.time.set_timer(MOVIMIENTO_UPDATE,150)

main_juego = JUEGO()

movimiento_previo = ""

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == MOVIMIENTO_UPDATE:
            if main_juego.mov():
                corriendo = False
        if event.type == pygame.KEYDOWN:
            if movimiento_previo != "DN" and event.key == pygame.K_UP or event.key == pygame.K_w:
                movimiento_previo = "UP"
                main_juego.snake.direccion = Vector2(0,-1)
            if movimiento_previo != "UP" and event.key == pygame.K_DOWN or event.key == pygame.K_s:
                movimiento_previo = "DN"
                main_juego.snake.direccion = Vector2(0,1)
            if movimiento_previo != "LT" and event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                movimiento_previo = "RT"
                main_juego.snake.direccion = Vector2(1,0)
            if movimiento_previo != "RT" and event.key == pygame.K_LEFT or event.key == pygame.K_a:
                movimiento_previo = "LT"
                main_juego.snake.direccion = Vector2(-1,0)

    screen.fill((175,215,70))
    main_juego.elementos()
    tempo.tick(60)
    pygame.display.update()
pygame.quit()