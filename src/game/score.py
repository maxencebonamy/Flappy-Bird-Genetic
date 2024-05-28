from utils.image import resize_image_keep_aspect


class Score:

	IMAGE_PATH = "assets/{index}.png"
	RESIZE_RATIO = 36 / 512

	def __init__(self, screen_height):
		self.__score = 0

		self.__images = [resize_image_keep_aspect(Score.IMAGE_PATH.format(index=i), int(screen_height * Score.RESIZE_RATIO)) for i in range(10)]

	def increase(self):
		self.__score += 1

	def get(self):
		return self.__score

	def draw(self, screen):
		score_str = str(self.__score)
		score_x = 20
		for digit in score_str:
			screen.blit(self.__images[int(digit)], (score_x, 20))
			score_x += self.__images[int(digit)].get_width() + 2