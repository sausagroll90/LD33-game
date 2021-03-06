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
		self.c_level = 0
		self.player = src.player.Player()
		self.enemy = src.enemy.Enemy(50, 1000000, 60)
		self.pause_countdown = 180
		self.c_menubutton = 1
		self.sound = {
			"hit" : pygame.mixer.Sound("res/hit.wav"),
			"block" : pygame.mixer.Sound("res/block.wav"),
			"mcharge" : pygame.mixer.Sound("res/mcharge.wav"),
			"magic" : pygame.mixer.Sound("res/mshot.wav"),
			"parry" : pygame.mixer.Sound("res/mparry.wav")
		}
		self.drects = []
		self.need_to_update = True
		self.magic_hit = False

	def handle_keypress(self, key):
		if key == pygame.K_UP or key == pygame.K_LEFT or key == pygame.K_RIGHT:
			self.player.handle_keypress(key, self)
			self.drects.append(pygame.Rect(500, 120, 300, 300))
		if key == pygame.K_ESCAPE:
			self.statestack.pop()
			self.c_level = 1
			self.need_to_update = True
			self.drects.append(pygame.Rect(0, 0, 1000, 600))

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.handle_keypress(event.key)

	def enemy_attack(self):
		self.countdown = self.enemy.cooldown

	def player_attack(self):
		self.sound["hit"].play()
		self.enemy.health -= 10
		self.drects.append(pygame.Rect(178, 518, 270, 30))
		self.drects.append(pygame.Rect(500, 120, 300, 300))

	def combat_handler(self):
		if self.enemy.action == "attack":
			if not self.player.action == "block":
				self.sound["hit"].play()
				self.player.health -= 10
				self.drects.append(pygame.Rect(552, 518, 270, 30))
			else:
				self.sound["block"].play()
		if self.enemy.action == "magic":
			if self.player.action == "parry":
				self.enemy.health -= 20
				self.sound["parry"].play()
				self.magic_hit = False
				self.drects.append(pygame.Rect(178, 518, 270, 30))
			else:
				self.player.health -= 20
				self.sound["magic"].play()
				self.magic_hit = True
				self.drects.append(pygame.Rect(552, 518, 270, 30))

	def lose_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.statestack.pop()
					self.statestack.pop()
					self.c_level = 1
					self.need_to_update = True
		self.screen.blit(losescreen, (0, 0))
		pygame.display.flip()

	def win_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.statestack.pop()
					self.statestack.pop()
					self.c_level = 1
					self.need_to_update = True
		self.screen.blit(winscreen, (0, 0))
		pygame.display.flip()

	def pause_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
		if self.need_to_update or self.updatenf:
			self.screen.blit(lvlimgs[self.c_level], (0, 0))
			pygame.display.flip()
			self.need_to_update = False
			self.updatenf = False
		if self.pause_countdown == 0:
			self.need_to_update = True
			self.statestack.pop()
		else:
			self.pause_countdown -= 1

	def next_level(self):
		if self.c_level == 0:
			self.enemy = src.enemy.Enemy(50, 23123124, 60)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
			self.updatenf = True
		elif self.c_level == 1:
			self.enemy = src.enemy.Enemy(100, 120, 60)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
			self.updatenf = True
		elif self.c_level == 2:
			self.enemy = src.enemy.Enemy(150, 110, 50)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
			self.updatenf = True
		elif self.c_level == 3:
			self.enemy = src.enemy.Enemy(200, 100, 40)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
			self.updatenf = True
		elif self.c_level == 4:
			self.enemy = src.enemy.Enemy(250, 80, 30)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
			self.updatenf = True
		elif self.c_level == 5:
			self.enemy = src.enemy.Enemy(300, 60, 30)
			self.pause_countdown = 180
			self.statestack.append(self.pause_state)
			self.updatenf = True

	def game_updates(self):
		self.player.update(self)
		self.enemy.update(self)
		if self.countdown > -1:
			self.countdown -= 1
		if self.countdown == 0:
			self.combat_handler()
		if self.player.health <= 0:
			self.statestack.append(self.lose_state)
		elif self.enemy.health <= 0:
			if not self.c_level >= 5:
				self.c_level += 1
				self.next_level()
			else:
				self.statestack.append(self.win_state)

	def draw_to_screen(self):
		self.screen.blit(background, (0, 0))
		self.player.draw(self.screen)
		self.enemy.draw(self.screen)
		if self.enemy.action == "magic":
			if self.enemy.countup == 0:
				self.screen.blit(magicball, (360, 290))
				self.drects.append(pygame.Rect(360, 290, 60, 60))
			elif self.enemy.countup < 10:
				if self.magic_hit:
					self.screen.blit(magicball, (635, 290))
					self.drects.append(pygame.Rect(635, 290, 60, 60))
					self.drects.append(pygame.Rect(360, 290, 60, 60))
				else:
					self.screen.blit(magicball, (580, 290))
					self.drects.append(pygame.Rect(580, 290, 60, 60))
					self.drects.append(pygame.Rect(360, 290, 60, 60))
			elif self.enemy.countup == 10:
				self.drects.append(pygame.Rect(550, 290, 300, 60))
		pygame.draw.rect(self.screen, (200, 0, 0), (178, 518, (self.enemy.health / float((self.c_level + 1) * 50)) * 270, 30))
		pygame.draw.rect(self.screen, (200, 0, 0), (552, 518, (self.player.health / 100.0) * 270, 30))
		if self.need_to_update:
			pygame.display.flip()
			self.need_to_update = False
		pygame.display.update(self.drects)

	def game_state(self):
		self.handle_events()
		self.game_updates()
		self.draw_to_screen()

	def menu_up(self):
		self.c_menubutton -= 1
		if self.c_menubutton == 0:
			self.c_menubutton = 2

	def menu_down(self):
		self.c_menubutton += 1
		if self.c_menubutton == 3:
			self.c_menubutton = 1

	def menu_enter(self):
		if self.c_menubutton == 1:
			self.statestack.append(self.game_state)
			self.next_level()
			self.player.health = 100
			self.updatenf = True
		elif self.c_menubutton == 2:
			self.done = True

	def menu_keypress(self, key):
		if key == pygame.K_UP:
			self.menu_up()
		elif key == pygame.K_DOWN:
			self.menu_down()
		elif key == pygame.K_RETURN or key == pygame.K_SPACE:
			self.menu_enter()
		elif key == pygame.K_ESCAPE:
			self.done = True

	def menu_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				self.menu_keypress(event.key)

	def menu_draw(self):
		self.screen.blit(menuimg, (0, 0))
		if self.c_menubutton == 1:
			self.screen.blit(menuselectimg, (300, 232))
		elif self.c_menubutton == 2:
			self.screen.blit(menuselectimg, (300, 375))
		pygame.display.flip()


	def menu_state(self):
		self.updatenf = False
		self.menu_events()
		self.menu_draw()
		if self.updatenf == True:
			self.need_to_update = True

	def main_loop(self):
		pygame.mixer.music.play(-1)
		while not self.done:
			if not self.statestack:
				self.statestack.append(self.menu_state)
			self.drects = []
			self.statestack[-1]()
			self.clock.tick(60)