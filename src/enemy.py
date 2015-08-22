import pygame
import random
import src.spritesheet_loader

class Enemy:
	def __init__(self):
		self.sprites = src.spritesheet_loader.load_spritesheet(pygame.image.load("res/placeholder2.png"), 300, 4, 1)
		self.img = {"neutral" : self.sprites[0], "attack" : self.sprites[1], "block" : self.sprites[2], "magic" : self.sprites[3]}
		self.c_img = self.img["neutral"]
		self.action = False
		self.statestack = []
		self.countdown = 120
		self.health = 100

	def cooldown_state(self, gameloop):
		self.countdown -= 1
		if self.countdown == 0:
			self.statestack.pop()
			self.countdown = 120

	def attack(self):
		self.action = "attack"
		self.c_img = self.img["attack"]
		self.countdown = 60
		self.statestack.append(self.cooldown_state)

	def magic(self):
		self.action = "magic"
		self.c_img = self.img["magic"]
		self.countdown = 60
		self.statestack.append(self.cooldown_state)

	def blocking_state(self, gameloop):
		self.action = "block"
		self.c_img = self.img["block"]
		self.countdown -= 1
		if self.countdown == 0:
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
		screen.blit(self.c_img, (100, 150))