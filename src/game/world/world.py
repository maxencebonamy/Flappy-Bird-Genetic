from game.world.background import Background
from game.world.pipe import Pipe
from game.player import Player
import random

class World:

	SPEED = 1
	MIN_PIPE_GAP = 180
	MAX_PIPE_GAP = 320
	INITIAL_PIPES = 2
	
	def __init__(self, screen_width, screen_height):
		self.__screen_width = screen_width
		self.__screen_height = screen_height

		self.__background = Background(screen_width, screen_height, World.SPEED)
		self.__pipes = []
		self.__next_gap = self.__get_next_gap()
  
		self.__init_pipes()

	def update(self):
		self.__background.update()

		for pipe in self.__pipes:
			pipe.update()

		self.__pipes = [pipe for pipe in self.__pipes if pipe.get_x() + pipe.get_width() > 0]

		if len(self.__pipes) == 0 or self.__pipes[-1].get_x() < self.__screen_width - self.__next_gap:
			self.__add_pipe(self.__screen_width)
			self.__next_gap = self.__get_next_gap()

	def draw(self, screen):
		self.__background.draw(screen)

		for pipe in self.__pipes:
			pipe.draw(screen)
	
	def collide(self, player):
		for pipe in self.__pipes[:2]:
			if pipe.collide(player):
				return True
		return False

	def players_passed_pipe(self):
		for pipe in self.__pipes:
			if pipe.get_x() + pipe.get_width() < Player.X_POSITION - 20 and not pipe.is_passed():
				pipe.set_passed()
				return True
		return False

	def get_next_pipe(self):
		for pipe in self.__pipes:
			if not pipe.is_passed():
				return pipe
		return None

	def __init_pipes(self):
		self.__add_pipe(self.__screen_width // 2)
		for i in range(World.INITIAL_PIPES - 1):
			last_pipe = self.__pipes[-1]
			self.__add_pipe(last_pipe.get_x() + last_pipe.get_width() + self.__next_gap)
			self.__next_gap = self.__get_next_gap()

	def __add_pipe(self, x):
		new_pipe = Pipe(x, self.__screen_height, World.SPEED * 2)
		self.__pipes.append(new_pipe)
	
	def __get_next_gap(self):
		return random.randint(World.MIN_PIPE_GAP, World.MAX_PIPE_GAP)