import pygame
from src.setup import *
import src.gameloop

mainloop = src.gameloop.Gameloop(screen, False, clock)

mainloop.main_loop()

pygame.quit()