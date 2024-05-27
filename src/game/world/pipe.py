from utils.image import resize_image_keep_aspect
import random
import pygame

class Pipe:

	GAP = 200
	IMAGE_PATH = "assets/pipe.png"
	RESIZE_RATIO = 320 / 512

	def __init__(self, screen_width, screen_height, speed):
		self.image_bottom = resize_image_keep_aspect(Pipe.IMAGE_PATH, int(screen_height * Pipe.RESIZE_RATIO))
		self.image_top = pygame.transform.rotate(self.image_bottom, 180)

		self.width = self.image_top.get_width()
		self.height = self.image_top.get_height()

		self.passed = False
		self.speed = speed
		self.x = screen_width
		self.y_top = random.randint(-300, -50)
		self.y_bottom = self.y_top + self.height + Pipe.GAP

	def update(self):
		self.x -= self.speed

	def draw(self, screen):
		screen.blit(self.image_top, (self.x, self.y_top))
		screen.blit(self.image_bottom, (self.x, self.y_bottom))
	
	def collide(self, player):
		top_rect = pygame.Rect(self.x, self.y_top, self.width, self.height)
		bottom_rect = pygame.Rect(self.x, self.y_bottom, self.width, self.height)

		return player.rect.colliderect(top_rect) or player.rect.colliderect(bottom_rect)
