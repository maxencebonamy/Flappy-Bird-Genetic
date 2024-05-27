from utils.image import resize_image_keep_aspect
import random
import pygame

class Pipe:

	GAP = 200
	IMAGE_PATH = "assets/pipe.png"
	RESIZE_RATIO = 320 / 512

	def __init__(self, screen_width, screen_height, speed):
		self.__image_bottom = resize_image_keep_aspect(Pipe.IMAGE_PATH, int(screen_height * Pipe.RESIZE_RATIO))
		self.__image_top = pygame.transform.rotate(self.__image_bottom, 180)

		self.__width = self.__image_top.get_width()
		self.__height = self.__image_top.get_height()

		self.__passed = False
		self.__speed = speed
		self.__x = screen_width
		self.__y_top = random.randint(-300, -50)
		self.__y_bottom = self.__y_top + self.__height + Pipe.GAP

	def update(self):
		self.__x -= self.__speed

	def draw(self, screen):
		screen.blit(self.__image_top, (self.__x, self.__y_top))
		screen.blit(self.__image_bottom, (self.__x, self.__y_bottom))
	
	def collide(self, player):
		top_rect = pygame.Rect(self.__x, self.__y_top, self.__width, self.__height)
		bottom_rect = pygame.Rect(self.__x, self.__y_bottom, self.__width, self.__height)

		return player.collide(top_rect) or player.collide(bottom_rect)

	def is_passed(self):
		return self.__passed
 
	def set_passed(self):
		self.__passed = True
	
	def get_x(self):
		return self.__x

	def get_width(self):
		return self.__width

	def get_gap_center_y(self):
		return self.__y_top + self.__height + Pipe.GAP // 2