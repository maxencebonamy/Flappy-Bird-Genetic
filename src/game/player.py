from utils.image import resize_image_keep_aspect
import pygame


class Player:

	IMAGE_PATH = "assets/bird-midflap.png"
	GRAVITY = 0.5
	JUMP_STRENGTH = -10
	RESIZE_RATIO = 24 / 512

	def __init__(self, screen_height, game):
		self.image = resize_image_keep_aspect(Player.IMAGE_PATH, int(screen_height * Player.RESIZE_RATIO))
		self.rect = self.image.get_rect(center=(100, screen_height // 2))
		self.y_velocity = 0
		self.game = game
	
	def on_key_down(self, key):
		if key == pygame.K_SPACE:
			self.jump()

	def jump(self):
		self.y_velocity = Player.JUMP_STRENGTH

	def update(self):
		self.y_velocity += Player.GRAVITY
		self.rect.centery += self.y_velocity

		if self.rect.top <= 0 or self.rect.bottom >= self.game.screen.get_height():
			self.game.game_over()

	def draw(self, screen):
		screen.blit(self.image, self.rect)