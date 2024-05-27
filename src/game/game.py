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
	SCREEN_FPS = 60
	SCREEN_TITLE = "Flappy Bird - FPS: {fps}"
	GAME_OVER_IMAGE_PATH = "assets/gameover.png"
	GAME_OVER_RESIZE_RATIO = 42 / 512

	def __init__(self):
		pygame.init()

		self.__screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
		self.__clock = pygame.time.Clock()
		pygame.display.set_caption(Game.SCREEN_TITLE.format(fps=self.__clock.get_fps()))

		self.__game_over_image = resize_image_keep_aspect(Game.GAME_OVER_IMAGE_PATH, int(Game.SCREEN_HEIGHT * Game.GAME_OVER_RESIZE_RATIO))
		self.__game_over_rect = self.__game_over_image.get_rect(center=(Game.SCREEN_WIDTH // 2, Game.SCREEN_HEIGHT // 2))

		self.__world = World(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
		self.__player = Player(Game.SCREEN_HEIGHT, self)
		self.score = Score(Game.SCREEN_HEIGHT)

		self.__state = GameState.IDLE
	
	def game_over(self):
		self.__state = GameState.GAME_OVER

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.__state == GameState.IDLE:
					self.__state = GameState.PLAYING
				self.__player.on_key_down(event.key)
		
		if self.__state == GameState.PLAYING:
			self.__world.update()
			self.__player.update()
			if self.__world.collide(self.__player):
				self.game_over()
			if self.__world.player_passed_pipe(self.__player):
				self.score.add(1)

		self.__screen.fill((0, 0, 0))
		self.__world.draw(self.__screen)
		if self.__state == GameState.GAME_OVER:
			self.__draw_dark_surface()
			self.__screen.blit(self.__game_over_image, self.__game_over_rect)
		else:
			self.__player.draw(self.__screen)
		self.score.draw(self.__screen)

		pygame.display.flip()
		self.__clock.tick(Game.SCREEN_FPS) / 1000
		pygame.display.set_caption(Game.SCREEN_TITLE.format(fps=self.__clock.get_fps()))

	def __draw_dark_surface(self):
		darken_rect = pygame.Surface((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
		darken_rect.set_alpha(200)
		darken_rect.fill((0, 0, 0))
		self.__screen.blit(darken_rect, (0, 0))