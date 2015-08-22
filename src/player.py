import pygame
import src.spritesheet_loader

class Player:
	def __init__(self):
		self.sprites = src.spritesheet_loader.load_spritesheet(pygame.image.load("res/placeholder.png"), 300, 4, 1)
		self.img = {"neutral" : self.sprites[0], "attack" : self.sprites[1], "block" : self.sprites[2], "parry" : self.sprites[3]}
		self.c_img = self.img["neutral"]
		self.action = False
		self.statestack = []
		self.countdown = 0
		self.health = 100

	def cooldown_state(self):
		self.countdown -= 1
		if self.countdown == 0:
			self.statestack.pop()

	def lkey(self, gameloop):
		self.action = "attack"
		self.c_img = self.img["attack"]
		self.countdown = 30
		self.statestack.append(self.cooldown_state)
		gameloop.player_attack()

	def ukey(self):
		self.action = "parry"
		self.c_img = self.img["parry"]
		self.countdown = 30
		self.statestack.append(self.cooldown_state)

	def rkey(self):
		self.action = "block"
		self.c_img = self.img["block"]
		self.countdown = 30
		self.statestack.append(self.cooldown_state)

	def handle_keypress(self, key, gameloop):
		if self.statestack[-1] == self.ready_state:
			if key == pygame.K_LEFT:
				self.lkey(gameloop)
			elif key == pygame.K_RIGHT:
				self.rkey()
			elif key == pygame.K_UP:
				self.ukey()

	def ready_state(self):
		self.c_img = self.img["neutral"]
		self.action = "neutral"

	def update(self):
		if not self.statestack:
			self.statestack.append(self.ready_state)
		self.statestack[-1]()

	def draw(self, screen):
		screen.blit(self.c_img, (600, 150))
