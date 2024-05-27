from game.world import World
from game.player import Player
import pygame
import sys

class Game:

	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 720

	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Flappy Bird")

		self.world = World(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
		self.player = Player(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)

		self.running = False

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if not self.running:
					self.running = True
				self.player.on_key_down(event.key)
		
		if self.running:
			self.world.update()
			self.player.update()

		self.screen.fill((0, 0, 0))
		self.world.draw(self.screen)
		self.player.draw(self.screen)
		pygame.display.flip()

		self.clock.tick(60)