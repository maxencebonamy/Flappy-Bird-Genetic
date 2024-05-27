from game.world.background import Background

class World:
    
	def __init__(self, screen_width, screen_height):
		self.background = Background(screen_width, screen_height, speed=2)

	def update(self):
		self.background.update()

	def draw(self, screen):
		self.background.draw(screen)