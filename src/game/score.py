from utils.image import resize_image_keep_aspect


class Score:

	RESIZE_RATIO = 36 / 512

	def __init__(self, screen_height):
		self.__score = 0

		self.__images = [resize_image_keep_aspect(f"assets/{i}.png", int(screen_height * Score.RESIZE_RATIO)) for i in range(10)]

	def add(self, points):
		self.__score += points

	def get(self):
		return self.__score

	def draw(self, screen):
		score_str = str(self.__score)
		score_x = 10
		for digit in score_str:
			screen.blit(self.__images[int(digit)], (score_x, 10))
			score_x += self.__images[int(digit)].get_width() + 2