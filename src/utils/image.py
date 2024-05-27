import pygame
from math import floor


def resize_image_keep_aspect(image_path, target_height):
    image = pygame.image.load(image_path)
    
    original_width = image.get_width()
    original_height = image.get_height()
    
    aspect_ratio = original_width / original_height
    new_width = floor(target_height * aspect_ratio)
    
    resized_image = pygame.transform.scale(image, (new_width, target_height))
    
    return resized_image.convert_alpha()