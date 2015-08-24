import pygame
import src.player
import src.enemy

pygame.mixer.pre_init(22050, -16, 2, 512)

pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("LD33")
clock = pygame.time.Clock()

lvlimgs = [
	pygame.image.load("res/level0.png"),
	pygame.image.load("res/level1.png"),
	pygame.image.load("res/level2.png"),
	pygame.image.load("res/level3.png"),
	pygame.image.load("res/level4.png"),
	pygame.image.load("res/level5.png")
]

magicball = pygame.image.load("res/anim/magic ball.png").convert_alpha()
winscreen = pygame.image.load("res/win.png")
losescreen = pygame.image.load("res/lose.png")
menuimg = pygame.image.load("res/menu.png")
background = pygame.image.load("res/background.png")
menuselectimg = pygame.image.load("res/menupicker.png").convert()
menuselectimg.set_colorkey((0, 255, 0))

theme = pygame.mixer.music.load("res/theme.mp3")
pygame.mixer.music.set_volume(0.3)