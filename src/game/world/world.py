from game.world.background import Background
from game.world.pipe import Pipe
import random

class World:

	SPEED = 2
	MIN_PIPE_GAP = 200
	MAX_PIPE_GAP = 500
	
	def __init__(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height

		self.background = Background(screen_width, screen_height, World.SPEED)
		self.pipes = []
		self.next_gap = self.__get_next_gap()

	def update(self):
		self.background.update()

		for pipe in self.pipes:
			pipe.update()

		self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]

		if len(self.pipes) == 0 or self.pipes[-1].x < self.screen_width - self.next_gap:
			self.__add_pipe()
			self.next_gap = self.__get_next_gap()

	def draw(self, screen):
		self.background.draw(screen)

		for pipe in self.pipes:
			pipe.draw(screen)
	
	def collide(self, player):
		for pipe in self.pipes:
			if pipe.collide(player):
				return True
		return False

	def __add_pipe(self):
		new_pipe = Pipe(self.screen_width, self.screen_height, World.SPEED)
		self.pipes.append(new_pipe)
	
	def __get_next_gap(self):
		return random.randint(World.MIN_PIPE_GAP, World.MAX_PIPE_GAP)