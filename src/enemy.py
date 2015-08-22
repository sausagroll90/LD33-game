import pygame
import random

class Enemy:
	def __init__(self):
		self.action = False
		self.statestack = []
		self.countdown = 120
		self.colour = (0, 0, 0)

	def cooldown_state(self):
		self.countdown -= 1
		if self.countdown == 0:
			self.statestack.pop()
			self.countdown = 120

	def attack(self):
		self.action = "attack"
		self.colour = (255, 0, 0)
		self.countdown = 60
		self.statestack.append(self.cooldown_state)

	def magic(self):
		self.action = "magic"
		self.colour = (0, 255, 0)
		self.countdown = 60
		self.statestack.append(self.cooldown_state)

	def blocking_state(self):
		self.colour = (0, 0, 255)
		self.countdown -= 1
		if self.countdown == 0:
			random.seed()
			choice = random.randint(1, 2)
			if choice == 1:
				self.attack()
			elif choice == 2:
				self.magic()

	def update(self):
		if not self.statestack:
			self.statestack.append(self.blocking_state)
		self.statestack[-1]()

	def draw(self, screen):
		pygame.draw.rect(screen, self.colour, (330, 250, 70, 100))