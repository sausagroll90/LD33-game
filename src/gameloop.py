import pygame
from src.setup import *

class Gameloop:
	def __init__(self, screen, done, clock):
		self.screen = screen
		self.done = done
		self.clock = clock

	def handle_keypress(self, key):
		if key == pygame.K_UP or key == pygame.K_LEFT or key == pygame.K_RIGHT:
			player.handle_keypress(key)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.handle_keypress(event.key)

	def do_updates(self):
		player.update()
		enemy.update()

	def draw_to_screen(self):
		self.screen.fill((255, 255, 255))
		player.draw(self.screen)
		enemy.draw(self.screen)
		pygame.display.flip()

	def main_loop(self):
		while not self.done:
			self.handle_events()
			self.do_updates()
			self.draw_to_screen()
			self.clock.tick(60)