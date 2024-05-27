from game.world import World
from game.player import Player
from game.game_state import GameState
from game.score import Score
from utils.image import resize_image_keep_aspect
import pygame
import sys

class Game:

	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 720
	GAME_OVER_IMAGE_PATH = "assets/gameover.png"
	GAME_OVER_RESIZE_RATIO = 42 / 512

	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Flappy Bird")

		self.game_over_image = resize_image_keep_aspect(Game.GAME_OVER_IMAGE_PATH, int(Game.SCREEN_HEIGHT * Game.GAME_OVER_RESIZE_RATIO))
		self.game_over_rect = self.game_over_image.get_rect(center=(Game.SCREEN_WIDTH // 2, Game.SCREEN_HEIGHT // 2))

		self.world = World(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
		self.player = Player(Game.SCREEN_HEIGHT, self)
		self.score = Score(Game.SCREEN_HEIGHT)

		self.state = GameState.IDLE
	
	def game_over(self):
		self.state = GameState.GAME_OVER

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.state == GameState.IDLE:
					self.state = GameState.PLAYING
				self.player.on_key_down(event.key)
		
		if self.state == GameState.PLAYING:
			self.world.update()
			self.player.update()
			if self.world.collide(self.player):
				self.game_over()
			if self.world.player_passed_pipe(self.player):
				self.score.add(1)

		self.screen.fill((0, 0, 0))
		self.world.draw(self.screen)
		self.player.draw(self.screen)
		if self.state == GameState.GAME_OVER:
			self.screen.blit(self.game_over_image, self.game_over_rect)
		self.score.draw(self.screen)
		pygame.display.flip()

		self.clock.tick(60)