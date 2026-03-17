import pygame
from logger import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
	def __init__(self, x, y, radius):

		if hasattr(self, "containers"):
			super().__init__(self.containers)
		else:
			super().__init__()

		self.position = pygame.Vector2(x, y)
		self.velocity = pygame.Vector2(0, 0)
		self.radius = radius

	def draw(self, screen):
		pass

	def update(self, dt):
		pass
		
	def collides_with(self, other):
		distance = self.position.distance_to(other.position)
		r1 = self.radius
		r2 = other.radius
		
		if distance <= (r1 + r2):
			return True
		else:
			return False
		
        

