from utils.image import resize_image_keep_aspect

class Background:

	IMAGE_PATH = "assets/background.png"

	def __init__(self, screen_width, screen_height, speed):
		self.__image = resize_image_keep_aspect(Background.IMAGE_PATH, screen_height)
		self.__width = self.__image.get_width()
		self.__height = self.__image.get_height()
		self.__speed = speed

		self.__images = []
		for i in range((screen_width // self.__width) + 2):
			self.__images.append((i * self.__width, 0))

	def update(self):
		for i in range(len(self.__images)):
			self.__images[i] = (self.__images[i][0] - self.__speed, self.__images[i][1])

		for i in range(len(self.__images)):
			if self.__images[i][0] <= -self.__width:
				max_x = max(self.__images, key=lambda x: x[0])[0]
				self.__images[i] = (max_x + self.__width, self.__images[i][1])

	def draw(self, screen):
		for pos in self.__images:
			screen.blit(self.__image, pos)
