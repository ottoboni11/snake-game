import pygame

sonido_menu = pygame.mixer.Sound("assets/sounds/ButtonSound.ogg") 
musica_fondo = pygame.mixer.Sound("assets/music/back.mp3")

canal_sonido_1 = pygame.mixer.Channel(1)
canal_sonido_2 = pygame.mixer.Channel(2)
canal_sonido_1.play(musica_fondo)
musica_fondo.set_volume(0.2)