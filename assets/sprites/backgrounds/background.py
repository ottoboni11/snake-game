import pygame
from assets.config.screen import cell_n, cell_size

background_menu = pygame.image.load("assets/sprites/backgrounds/background_menu.jpg")
background_menu = pygame.transform.scale(background_menu, (cell_n * cell_size, cell_n * cell_size))

background_image = pygame.image.load("assets/sprites/backgrounds/background.jpg")
background_image = pygame.transform.scale(background_image, (cell_n * cell_size, cell_n * cell_size))