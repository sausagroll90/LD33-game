import pygame

class Player:
	def __init__(self):
		self.img = {
			"neutral" : pygame.image.load("res/anim/monster - neutral.png").convert_alpha(),
			"attack" : pygame.image.load("res/anim/monster - attack.png").convert_alpha(),
			"block" : pygame.image.load("res/anim/monster - block.png").convert_alpha(),
			"parry" : pygame.image.load("res/anim/monster - parry.png").convert_alpha()
		}
		self.c_img = self.img["neutral"]
		self.action = False
		self.statestack = []
		self.countdown = 0
		self.health = 100

	def cooldown_state(self, gameloop):
		self.countdown -= 1
		if self.action == "attack" and self.countdown == 25:
			self.c_img = self.img["block"]
			gameloop.drects.append(pygame.Rect(500, 120, 300, 300))
		if self.countdown <= 0:
			gameloop.drects.append(pygame.Rect(500, 120, 300, 300))
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
		screen.blit(self.c_img, (500, 120))
