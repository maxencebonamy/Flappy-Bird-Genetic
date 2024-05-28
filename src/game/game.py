from game.world import World
from game.player import Player
from game.game_state import GameState
from game.score import Score
from utils.image import resize_image_keep_aspect
from typing import List
import pygame
import sys

class Game:

	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 720
	SCREEN_FPS = 60
	SCREEN_TITLE = "Flappy Bird - FPS: {fps} - ALIVE PLAYERS: {alive}"
	SCREEN_ICON_PATH = "assets/icon.png"
	GAME_OVER_IMAGE_PATH = "assets/gameover.png"
	GAME_OVER_RESIZE_RATIO = 42 / 512
	MANUAL_MODE = False
	MAX_SCORE = 30

	def __init__(self):
		pygame.init()

		self.__screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
		self.__clock = pygame.time.Clock()
		pygame.display.set_caption(Game.SCREEN_TITLE.format(fps=self.__clock.get_fps(), alive=0))
		icon = pygame.image.load(Game.SCREEN_ICON_PATH)
		pygame.display.set_icon(icon)

		self.__game_over_image = resize_image_keep_aspect(Game.GAME_OVER_IMAGE_PATH, int(Game.SCREEN_HEIGHT * Game.GAME_OVER_RESIZE_RATIO))
		self.__game_over_rect = self.__game_over_image.get_rect(center=(Game.SCREEN_WIDTH // 2, Game.SCREEN_HEIGHT // 2))

		self.__world = World(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
		self.__players = []
		self.__score = Score(Game.SCREEN_HEIGHT)
		self.__state = GameState.IDLE
  
		if Game.MANUAL_MODE:
			self.add_players(1)
	
	def start(self):
		self.__state = GameState.PLAYING
 
	def game_over(self):
		self.__state = GameState.GAME_OVER

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.__state == GameState.IDLE:
					self.start()
				if Game.MANUAL_MODE and event.key == pygame.K_SPACE:
					self.__players[0].jump()
		
		nb_players_alive = 0
		if self.__state == GameState.PLAYING:
			self.__world.update()
			update_score = False
			if self.__world.players_passed_pipe():
				self.__score.increase()
				update_score = True
				if self.__score.get() == Game.MAX_SCORE:
					self.game_over()
			for player in self.__players:
				if not player.is_game_over():
					player.update()
					if self.__world.collide(player):
						player.game_over()
					else:
						if update_score:
							player.increase_score()
						nb_players_alive += 1
			if nb_players_alive == 0:
				self.game_over()
  
		self.__screen.fill((0, 0, 0))
		self.__world.draw(self.__screen)
		if self.__state == GameState.GAME_OVER:
			self.__draw_dark_surface()
			self.__screen.blit(self.__game_over_image, self.__game_over_rect)
		else:
			for player in self.__players:
				if not player.is_game_over():
					player.draw(self.__screen)
		self.__score.draw(self.__screen)

		pygame.display.flip()
		self.__clock.tick(Game.SCREEN_FPS) / 1000
		pygame.display.set_caption(Game.SCREEN_TITLE.format(
	  		fps=round(self.__clock.get_fps()),
			alive=nb_players_alive
		))
	
	def is_game_over(self):
		return self.__state == GameState.GAME_OVER
 
	def get_global_score(self):
		return self.__score.get()

	def get_players(self) -> List[Player]:
		return self.__players

	def get_world(self):
		return self.__world

	def add_players(self, amount):
		for _ in range(amount):
			self.__players.append(Player(Game.SCREEN_HEIGHT, self.__world))

	def __draw_dark_surface(self):
		darken_rect = pygame.Surface((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
		darken_rect.set_alpha(200)
		darken_rect.fill((0, 0, 0))
		self.__screen.blit(darken_rect, (0, 0))