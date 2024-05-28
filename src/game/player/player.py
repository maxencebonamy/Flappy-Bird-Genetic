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
	X_POSITION = 100

	def __init__(self, screen_height, world):
		self.__images = {
      		state: resize_image_keep_aspect(Player.IMAGE_PATH.format(state=state.value), int(screen_height * Player.RESIZE_RATIO))
        	for state in PlayerState
		}
		self.__rect = self.__images[PlayerState.MIDFLAP].get_rect(center=(Player.X_POSITION, screen_height // 2))

		self.__y_velocity = 0
		self.__rotate_velocity = 0
		self.__state_index = 0
		self.__animation_counter = 0
		self.__game_over = False
		self.__score = 0

		self.__world = world
		self.__screen_height = screen_height
   
	def collide(self, rect):
		return self.__rect.colliderect(rect)

	def get_position(self):
		return self.__rect.center

	def get_y_velocity(self):
		return self.__y_velocity

	def jump(self):
		self.__y_velocity = Player.JUMP_STRENGTH
		self.__rotate_velocity = Player.JUMP_ROTATE

	def game_over(self):
		self.__game_over = True
	
	def is_game_over(self):
		return self.__game_over

	def increase_score(self):
		self.__score += 1

	def get_score(self):
		return self.__score

	def get_horizontal_distance_next_pipe(self):
		next_pipe = self.__world.get_next_pipe()
		if next_pipe:
			return next_pipe.get_x() - self.get_position()[0]
		return None

	def get_vertical_distance_next_pipe(self):
		next_pipe = self.__world.get_next_pipe()
		if next_pipe:
			return next_pipe.get_gap_center_y() - self.get_position()[1]
		return None

	def get_distance_to_ceil(self):
		return self.__rect.top

	def get_distance_to_floor(self):
		return self.__screen_height - self.__rect.bottom

	def update(self):
		self.__animation_counter += 1
		self.__y_velocity += Player.GRAVITY
		self.__rotate_velocity = max(self.__rotate_velocity - 2, -90)
		self.__rect.centery += self.__y_velocity
		if self.__animation_counter >= Player.ANIMATION_SPEED:
			self.__state_index = (self.__state_index + 1) % len(Player.STATES)
			self.__animation_counter = 0

		if self.__rect.top <= 0 or self.__rect.bottom >= self.__screen_height:
			self.game_over()

	def draw(self, screen):
		image = self.__images[Player.STATES[self.__state_index]]
		image = pygame.transform.rotate(image, self.__rotate_velocity)
		screen.blit(image, self.__rect)