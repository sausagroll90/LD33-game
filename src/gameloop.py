import pygame

class Gameloop:
	def __init__(self, screen, done, clock):
		self.screen = screen
		self.done = done
		self.clock = clock

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True

	def do_updates(self):
		pass

	def draw_to_screen(self):
		self.screen.fill((255, 255, 255))
		pygame.display.flip()

	def main_loop(self):
		while not self.done:
			self.handle_events()
			self.do_updates()
			self.draw_to_screen()
			self.clock.tick(60)