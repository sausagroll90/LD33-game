import pygame
import random
import src.spritesheet_loader

class Enemy:
	def __init__(self, health, countdown, cooldown):
		self.sprites = src.spritesheet_loader.load_spritesheet(pygame.image.load("res/placeholder2.png").convert(), 300, 4, 1)
		for img in self.sprites:
			img.set_colorkey((255, 255, 255))
		self.img = {
			"attack" : self.sprites[1],
			"block" : pygame.image.load("res/anim/hero - block.png").convert_alpha(),
			"neutral" : pygame.image.load("res/anim/hero - neutral.png").convert_alpha(),
			"magic" : pygame.image.load("res/anim/hero - charging magic.png").convert_alpha(),
			"magicfired" : pygame.image.load("res/anim/hero - fired magic.png").convert_alpha()
		}
		self.c_img = self.img["neutral"]
		self.action = False
		self.statestack = []
		self.countdowntime = countdown
		self.countdown = self.countdowntime
		self.health = health
		self.cooldown = cooldown
		self.magicsound = pygame.mixer.Sound("res/mcharge.wav")
		self.countup = 0

	def cooldown_state(self, gameloop):
		self.countup = 0
		self.countdown -= 1
		if self.countdown == 0:
			self.statestack.pop()
			self.countdown = self.countdowntime
			gameloop.drects.append(pygame.Rect(552, 518, 270, 30))
			if self.action == "magic":
				self.c_img = self.img["magicfired"]

	def attack(self):
		self.action = "attack"
		self.c_img = self.img["attack"]
		self.countdown = self.cooldown
		self.statestack.append(self.cooldown_state)

	def magic(self):
		self.action = "magic"
		self.c_img = self.img["magic"]
		self.countdown = self.cooldown
		self.statestack.append(self.cooldown_state)
		self.magicsound.play()

	def blocking_state(self, gameloop):
		self.countup += 1
		if self.countup > 20:
			self.action = "block"
			self.c_img = self.img["neutral"]
			gameloop.drects.append(pygame.Rect(250, 180, 300, 300))
		self.countdown -= 1
		if self.countdown == 0:
			gameloop.drects.append(pygame.Rect(250, 180, 300, 300))
			random.seed()
			choice = random.randint(1, 2)
			if choice == 1:
				self.attack()
			elif choice == 2:
				self.magic()
			gameloop.enemy_attack()

	def update(self, gameloop):
		if not self.statestack:
			self.statestack.append(self.blocking_state)
		self.statestack[-1](gameloop)

	def draw(self, screen):
		screen.blit(self.c_img, (250, 180))