import pygame
from src.setup import *
import src.enemy
import src.player

class Gameloop:
	def __init__(self, screen, done, clock):
		self.screen = screen
		self.done = done
		self.clock = clock
		self.countdown = 0
		self.statestack = []
		self.font = pygame.font.Font("res/FreeSansBold.ttf", 30)
		self.c_level = 1
		self.player = src.player.Player()
		self.enemy = src.enemy.Enemy(100, 120, 60)
		self.pause_countdown = 180

	def handle_keypress(self, key):
		if key == pygame.K_UP or key == pygame.K_LEFT or key == pygame.K_RIGHT:
			self.player.handle_keypress(key, self)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.handle_keypress(event.key)

	def enemy_attack(self):
		self.countdown = self.enemy.cooldown

	def player_attack(self):
		self.enemy.health -= 10

	def combat_handler(self):
		if self.enemy.action == "attack":
			if not self.player.action == "block":
				self.player.health -= 10
		if self.enemy.action == "magic":
			if self.player.action == "parry":
				self.enemy.health -= 20
			else:
				self.player.health -= 20

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

	def pause_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
		if self.pause_countdown == 0:
			self.statestack.pop()
		else:
			self.pause_countdown -= 1
		self.screen.blit(lvlimgs[self.c_level - 1], (0, 0))
		pygame.display.flip()

	def next_level(self):
		if self.c_level == 2:
			self.enemy = src.enemy.Enemy(150, 110, 50)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
		elif self.c_level == 3:
			self.enemy = src.enemy.Enemy(200, 100, 40)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
		elif self.c_level == 4:
			self.enemy = src.enemy.Enemy(250, 80, 30)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
		elif self.c_level == 5:
			self.enemy = src.enemy.Enemy(200, 60, 30)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)

	def game_updates(self):
		self.player.update()
		self.enemy.update(self)
		if self.countdown > -1:
			self.countdown -= 1
		if self.countdown == 0:
			self.combat_handler()
		if self.player.health <= 0:
			self.statestack.append(self.lose_state)
		elif self.enemy.health <= 0:
			print(self.c_level)
			if not self.c_level >= 5:
				self.c_level += 1
				self.next_level()
			else:
				self.statestack.append(self.win_state)
		self.playertext = self.font.render("health: " + str(self.player.health), False, (0, 0, 0))
		self.enemytext = self.font.render("health: " + str(self.enemy.health), False, (0, 0, 0))

	def draw_to_screen(self):
		self.screen.fill((255, 255, 255))
		self.player.draw(self.screen)
		self.enemy.draw(self.screen)
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
				self.statestack.append(self.pause_state)
			self.statestack[-1]()
			self.clock.tick(60)