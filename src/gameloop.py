import pygame
from src.setup import *

class Gameloop:
	def __init__(self, screen, done, clock):
		self.screen = screen
		self.done = done
		self.clock = clock
		self.countdown = 0
		self.statestack = []
		self.font = pygame.font.Font(None, 30)

	def handle_keypress(self, key):
		if key == pygame.K_UP or key == pygame.K_LEFT or key == pygame.K_RIGHT:
			player.handle_keypress(key, self)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.handle_keypress(event.key)

	def enemy_attack(self):
		self.countdown = 40

	def player_attack(self):
		enemy.health -= 10

	def combat_handler(self):
		if enemy.action == "attack":
			if not player.action == "block":
				player.health -= 10
		if enemy.action == "magic":
			if player.action == "parry":
				enemy.health -= 20
			else:
				player.health -= 20
		print(enemy.health, player.health)

	def lose_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
		screen.fill((255, 0, 0))
		pygame.display.flip()

	def win_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
		screen.fill((0, 255, 0))
		pygame.display.flip()

	def game_updates(self):
		player.update()
		enemy.update(self)
		if self.countdown > -1:
			self.countdown -= 1
		if self.countdown == 0:
			self.combat_handler()
		if player.health <= 0:
			self.statestack.append(self.lose_state)
		elif enemy.health <= 0:
			self.statestack.append(self.win_state)
		self.playertext = self.font.render("health: " + str(player.health), False, (0, 0, 0))
		self.enemytext = self.font.render("health: " + str(enemy.health), False, (0, 0, 0))

	def draw_to_screen(self):
		self.screen.fill((255, 255, 255))
		player.draw(self.screen)
		enemy.draw(self.screen)
		self.screen.blit(self.enemytext, (100, 100))
		self.screen.blit(self.playertext, (600, 100))
		pygame.display.flip()

	def game_state(self):
		self.handle_events()
		self.game_updates()
		self.draw_to_screen()

	def main_loop(self):
		while not self.done:
			if not self.statestack:
				self.statestack.append(self.game_state)
			self.statestack[-1]()
			self.clock.tick(60)