import pygame
import src.spritesheet_loader

class Player:
	def __init__(self):
		self.sprites = src.spritesheet_loader.load_spritesheet(pygame.image.load("res/placeholder.png").convert(), 300, 4, 1)
		for img in self.sprites:
			img.set_colorkey((255, 255, 255))
		self.img = {"neutral" : self.sprites[0], "attack" : self.sprites[1], "block" : self.sprites[2], "parry" : self.sprites[3]}
		self.c_img = self.img["neutral"]
		self.action = False
		self.statestack = []
		self.countdown = 0
		self.health = 100

	def cooldown_state(self, gameloop):
		self.countdown -= 1
		if self.countdown == 0:
			gameloop.drects.append(pygame.Rect(600, 150, 300, 300))
			self.statestack.pop()
			self.c_img = self.img["neutral"]

	def lkey(self, gameloop):
		self.action = "attack"
		self.c_img = self.img["attack"]
		self.countdown = 30
		self.statestack.append(self.cooldown_state)
		gameloop.player_attack()

	def ukey(self, gameloop):
		self.action = "parry"
		self.c_img = self.img["parry"]
		self.countdown = gameloop.countdown + 1
		self.statestack.append(self.cooldown_state)

	def rkey(self, gameloop):
		self.action = "block"
		self.c_img = self.img["block"]
		self.countdown = gameloop.countdown + 1
		self.statestack.append(self.cooldown_state)

	def handle_keypress(self, key, gameloop):
		if self.statestack[-1] == self.ready_state:
			if key == pygame.K_LEFT:
				self.lkey(gameloop)
			elif key == pygame.K_RIGHT:
				self.rkey(gameloop)
			elif key == pygame.K_UP:
				self.ukey(gameloop)

	def ready_state(self, gameloop):
		self.c_img = self.img["neutral"]
		self.action = "neutral"

	def update(self, gameloop):
		if not self.statestack:
			self.statestack.append(self.ready_state)
		self.statestack[-1](gameloop)

	def draw(self, screen):
		screen.blit(self.c_img, (600, 150))
