from utils.image import resize_image_keep_aspect

class Background:

	IMAGE_PATH = "assets/background.png"

	def __init__(self, screen_width, screen_height, speed):
		self.image = resize_image_keep_aspect(Background.IMAGE_PATH, screen_height)
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.speed = speed

		self.images = []
		for i in range((screen_width // self.width) + 2):
			self.images.append((i * self.width, 0))

	def update(self):
		for i in range(len(self.images)):
			self.images[i] = (self.images[i][0] - self.speed, self.images[i][1])

		for i in range(len(self.images)):
			if self.images[i][0] <= -self.width:
				max_x = max(self.images, key=lambda x: x[0])[0]
				self.images[i] = (max_x + self.width, self.images[i][1])

	def draw(self, screen):
		for pos in self.images:
			screen.blit(self.image, pos)
