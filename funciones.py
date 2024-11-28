import json
import pygame
from assets.config.screen import screen
from assets.font.fuentes import fuente_opciones
from assets.color.colores import BLANCO,AMARILLO,VERDE,VERDE_CLARO
from assets.sprites.backgrounds.background import background_menu
from assets.config.screen import boton_jugar, boton_ranking, boton_salir


def dibujar_texto(texto:str, x:int, y:int, color:tuple)->None:
    """
    Dibuja el texto en la pantalla en las coordenadas (x, y) con el color especificado.

    Parametros: - texto (str) es el texto a mostrar.
                - x (int): Es la coordenada x donde se dibujará el texto
                - y (int): Es la coordenada y donde se dibujará el texto
                - color (tupla): Color en formato RGB para el texto
    """
    superficie = fuente_opciones.render(texto, True, color)
    screen.blit(superficie, (x, y))


def mostrar_menu():
    '''
    Dibuja el menu en pantalla con sus respectivos elementos, titulo, menu, etc.
    Efecto hover en los botones.
    '''
    screen.blit(background_menu, (0, 0)) # Imprimimos el background del menu.
    dibujar_texto("El Juego De La Serpiente", 40, 130, BLANCO)

    # Botón Jugar
    # Si la posición actual de mouse se encuentra sobre el rectangulo del boton jugar.
    if boton_jugar.collidepoint(pygame.mouse.get_pos()): 
        pygame.draw.rect(screen, VERDE_CLARO, boton_jugar) # Dibuja un rectangulo con un color más claro (hover).
        
    else: # Caso contrario dibuja un rectangulo con un verde mas oscuro.
        pygame.draw.rect(screen, VERDE, boton_jugar) 
    dibujar_texto("Jugar", boton_jugar.x + 50, boton_jugar.y + 15, BLANCO) # Dibuja el texto de "Jugar"

    # Botón Ranking
    # Si la posición actual de mouse se encuentra sobre el rectangulo del boton ranking.
    if boton_ranking.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, VERDE_CLARO, boton_ranking)
        
    else:
        pygame.draw.rect(screen, VERDE, boton_ranking)
    dibujar_texto("Ranking", boton_ranking.x + 20, boton_ranking.y + 15, BLANCO)

    # Botón Salir
    if boton_salir.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, VERDE_CLARO, boton_salir)
        
    else:
        pygame.draw.rect(screen, VERDE, boton_salir)
    dibujar_texto("Salir", boton_salir.x + 50, boton_salir.y + 15, BLANCO)


# Función para mostrar la pantalla de ranking
def mostrar_ranking():
    """
    Muestra el ranking de puntuación de los jugadores cargando desde un archivo Json.
    A medida que la lista de ranking se vaya actualizando, se va ordenando por mayor puntuación.
    """
    screen.blit(background_menu, (0, 0)) # Imprimimos el background.
    dibujar_texto("Mejores 5 jugadores", 100, 100, AMARILLO)

    with open("ranking_puntuaciones.json", "r") as archivo: # Cargamos el json con el ranking de puntuaciones.
        ranking = json.load(archivo)

    if ranking == {}: # Si el json esta vacio, mostramos un mensaje.
        dibujar_texto("No hay jugadores.", 50, 200, BLANCO)
        dibujar_texto("ESC para volver", 50, 350, AMARILLO) 
    else:
        # Extraemos del json el nombre y la puntuación de los jugadores. Lo guardamos en una lista vacia.
        lista_ranking = []
        for jugador, datos in ranking.items():
            lista_ranking += [[datos["nombre"], datos["puntuacion"]]]

        # Ordenamos las lista de manera descendente.
        for i in range(len(lista_ranking)):
            for j in range(0, len(lista_ranking) - i - 1 ):
                if lista_ranking[j][1] < lista_ranking[j+1][1]:
                    lista_ranking[j], lista_ranking[j + 1] = lista_ranking [j + 1], lista_ranking[j]
        
        # Imprimos los datos en pantalla.
        ubicacion_y = 200 # Ubicación en Y principal.
        posicion = 1  # Posición del jugador en la lista.

        for nombre, puntuacion in lista_ranking[:5]: # Recorremos la lista hasta los primeros 5 jugadores
            texto = f"{posicion}. {nombre} - {puntuacion} puntos" 
            dibujar_texto(texto, 50, ubicacion_y, BLANCO)  
            ubicacion_y += 50 # Aumentamos la ubicación en Y para imprimir mas abajo al siguiente jugador.
            posicion += 1  # Aumentamos la posición para el siguiente jugador.

        # Imprimimos textos en pantalla
        dibujar_texto("R para resetear ", 50, 500, BLANCO) 
        dibujar_texto("la lista", 50, 550, BLANCO) 
        dibujar_texto("ESC para volver", 50, 650, AMARILLO) 


def resetear_ranking():
    '''
    Resetea el ranking de puntuaciones.

    Sobreescribe un diccionario vacio sobre el diccionario actual.
    '''
    with open("ranking_puntuaciones.json", "w") as archivo:
        json.dump({}, archivo, indent=4)


def agregar_jugador_ranking(nombre:str, puntuacion: float) -> None:
    '''
    Funcion que actualiza el archivo ranking_puntuaciones.json con los datos del nuevo jugador, obtenidos por los parámetros.

    Parámetros:
    Nombre del jugador: nuevo jugador (str)
    Puntuación de la partida: Puntuacion del nuevo jugador. (float)
    Cantidad de victorias: Victorias del nuevo jugador. (int)

    Abre el archivo en modo lectura y escritura (r+)
    Carga la informacion obtenida actualizando el archivo.
    '''
    with open("ranking_puntuaciones.json", mode="r+") as archivo:

        #Carga de contenido actual.
        lista_puntuaciones = json.load(archivo)

        #Corroboramos el numero del nuevo jugador en la lista.
        numero_nuevo_jugador = len(lista_puntuaciones)+1
        jugador_nuevo_key = f"jugador_{numero_nuevo_jugador}"
        
        #Se añade la informacion del jugador en el formato especificado abajo.
        lista_puntuaciones[jugador_nuevo_key] = {
            "nombre": f"{nombre}",
            "puntuacion": puntuacion,
        }

        #.seek(0) vuelve al inicio del JSON y escribe el archivo actualizado.
        archivo.seek(0)
        json.dump(lista_puntuaciones, archivo, indent=4)


def menu_final(puntuacion:int)-> None:
    '''
    Función que imprime en pantalla el menu final con la puntuación del jugador.

    Parámetros: 
    Puntuación: puntuacion del jugador (int)

    '''
    screen.blit(background_menu, (0, 0))
    dibujar_texto("Tu puntación:",200, 100, AMARILLO)
    dibujar_texto(f"{puntuacion} puntos",250, 200, BLANCO)
    dibujar_texto("R para volver a intentar", 40, 320, AMARILLO)
    dibujar_texto("G para guardar puntuación", 40, 380, AMARILLO)
    dibujar_texto("ESC para volver", 40, 600, AMARILLO) 



