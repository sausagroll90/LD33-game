import pygame
import src.player
import src.enemy

pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("LD33")
clock = pygame.time.Clock()

lvlimgs = [
	pygame.image.load("res/level1.png"),
	pygame.image.load("res/level2.png"),
	pygame.image.load("res/level3.png"),
	pygame.image.load("res/level4.png"),
	pygame.image.load("res/level5.png")
]