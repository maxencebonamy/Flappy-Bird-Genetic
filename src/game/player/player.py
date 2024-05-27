from utils.image import resize_image_keep_aspect
from game.player.player_state import PlayerState
import pygame


class Player:

	IMAGE_PATH = "assets/bird-{state}.png"
	GRAVITY = 0.5
	JUMP_STRENGTH = -10
	JUMP_ROTATE = 45
	RESIZE_RATIO = 24 / 512
	STATES = [PlayerState.DOWNFLAP, PlayerState.MIDFLAP, PlayerState.UPFLAP, PlayerState.MIDFLAP]
	ANIMATION_SPEED = 5

	def __init__(self, screen_height, game):
		self.__images = {
      		state: resize_image_keep_aspect(Player.IMAGE_PATH.format(state=state.value), int(screen_height * Player.RESIZE_RATIO))
        	for state in PlayerState
		}
		self.__rect = self.__images[PlayerState.MIDFLAP].get_rect(center=(100, screen_height // 2))

		self.__y_velocity = 0
		self.__rotate_velocity = 0
		self.__state_index = 0
		self.__animation_counter = 0
  
		self.__screen_height = screen_height
		self.__game = game
   
	def collide(self, rect):
		return self.__rect.colliderect(rect)

	def get_position(self):
		return self.__rect.center

	def get_y_velocity(self):
		return self.__y_velocity

	def jump(self):
		self.__y_velocity = Player.JUMP_STRENGTH
		self.__rotate_velocity = Player.JUMP_ROTATE

	def update(self):
		self.__animation_counter += 1
		self.__y_velocity += Player.GRAVITY
		self.__rotate_velocity = max(self.__rotate_velocity - 2, -90)
		self.__rect.centery += self.__y_velocity
		if self.__animation_counter >= Player.ANIMATION_SPEED:
			self.__state_index = (self.__state_index + 1) % len(Player.STATES)
			self.__animation_counter = 0

		if self.__rect.top <= 0 or self.__rect.bottom >= self.__screen_height:
			self.__game.game_over()

	def draw(self, screen):
		image = self.__images[Player.STATES[self.__state_index]]
		image = pygame.transform.rotate(image, self.__rotate_velocity)
		screen.blit(image, self.__rect)