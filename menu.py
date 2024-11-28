import pygame
from juego import iniciar_juego
from assets.sounds.sounds import sonido_menu
from funciones import resetear_ranking, mostrar_menu, mostrar_ranking, menu_final, agregar_jugador_ranking
from assets.config.screen import boton_jugar, boton_ranking, boton_salir

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("El Juego De La Serpiente")

# Bucle principal
estado = "menu"
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # Detectamos los clics en el menú
        if estado == "menu" and evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_jugar.collidepoint(evento.pos):
                sonido_menu.play()
                estado = "juego" # Actualizamos el estado en "juego"
            elif boton_ranking.collidepoint(evento.pos):
                sonido_menu.play()
                estado = "ranking" # Actualizamos el estado en "ranking"
            elif boton_salir.collidepoint(evento.pos):
                sonido_menu.play()
                corriendo = False # Detenemos el bucle, terminando el programa.

        # Si estamos en el ranking o en el menú final: Podemos volver al menú principal.
        if (estado == "ranking" or estado == "menu final") and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  #Tecla ESC para volver al menu.
                sonido_menu.play()
                estado = "menu"

        # Si estamos en el ranking: Podemos resetear las lista de puntuaciones.
        if estado == "ranking" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:  #Tecla R para resetear ranking.
                sonido_menu.play()
                resetear_ranking()
                mostrar_ranking()

        # Si estamos en el menú final: podemos volver a jugar o guardar la puntuación.
        if estado == "menu final" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:  #Tecla R para volver a jugar.
                estado = "juego"
            if evento.key == pygame.K_g: #Tecla G para guardar puntuación.
                sonido_menu.play()
                agregar_jugador_ranking("Serpentino",puntuacion)
                estado = "menu"


    # Dibuja en pantalla segun el estado.
    
    if estado == "menu":
        mostrar_menu()
    elif estado == "juego":
        juego_terminado = iniciar_juego() # Una vez terminado el juego, iniciar_juego() retorna una tupla = ("menu final", puntuacion)
        puntuacion = juego_terminado[1]
        estado = juego_terminado[0]
    elif estado == "ranking":
        mostrar_ranking()
    elif estado == "menu final":
        menu_final(puntuacion)

    # Actualiza la  pantalla
    pygame.display.flip()

# Salimos del programa
pygame.quit()
