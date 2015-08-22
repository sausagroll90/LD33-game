import pygame
import src.player
import src.enemy

pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("LD33")
clock = pygame.time.Clock()

player = src.player.Player()
enemy = src.enemy.Enemy()