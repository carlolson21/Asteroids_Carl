import random
from circleshape import *
from constants import *
from logger import *

class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)
		
	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
		
	def update(self, dt):
		self.position += (self.velocity * dt)
		
	def split(self):
		self.kill()
		if self.radius <= ASTEROID_MIN_RADIUS:
			return
		else:
			log_event("asteroid_split")
			rotate_angle = random.uniform(20, 50)
			asteroid_1_velocity = self.velocity.rotate(rotate_angle)
			asteroid_2_velocity = self.velocity.rotate(-rotate_angle)
			new_radius = self.radius - ASTEROID_MIN_RADIUS
			asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
			asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
			asteroid_1.velocity = asteroid_1_velocity * 1.2
			asteroid_2.velocity = asteroid_2_velocity * 1.2
		
