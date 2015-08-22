import pygame

class Player:
	def __init__(self):
		self.action = False
		self.statestack = []
		self.countdown = 0
		self.colour = (0, 0, 0)

	def cooldown_state(self):
		self.countdown -= 1
		if self.countdown == 0:
			self.statestack.pop()

	def lkey(self):
		self.action = "attack"
		self.colour = (255, 0, 0)
		self.countdown = 30
		self.statestack.append(self.cooldown_state)

	def ukey(self):
		self.action = "parry"
		self.colour = (0, 255, 0)
		self.countdown = 30
		self.statestack.append(self.cooldown_state)

	def rkey(self):
		self.action = "block"
		self.colour = (0, 0, 255)
		self.countdown = 30
		self.statestack.append(self.cooldown_state)

	def handle_keypress(self, key):
		if self.statestack[-1] == self.ready_state:
			if key == pygame.K_LEFT:
				self.lkey()
			elif key == pygame.K_RIGHT:
				self.rkey()
			elif key == pygame.K_UP:
				self.ukey()

	def ready_state(self):
		self.colour = (0, 0, 0)

	def update(self):
		if not self.statestack:
			self.statestack.append(self.ready_state)
		self.statestack[-1]()

	def draw(self, screen):
		pygame.draw.rect(screen, self.colour, (600, 250, 70, 100))
