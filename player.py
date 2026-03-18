from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		self.rotation = 0
		self.cooldown = 0
		self.booster = PLAYER_BOOSTER
		self.booster_cooldown = PLAYER_BOOSTER_COOLDOWN
		
	def triangle(self):
		forward = pygame.Vector2(0, 1).rotate(self.rotation)
		right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
		a = self.position + forward * self.radius
		b = self.position - forward * self.radius - right
		c = self.position - forward * self.radius + right
		return [a, b, c]
		
	def draw(self, screen):
		pygame.draw.polygon(screen, "green", self.triangle(), LINE_WIDTH)
		
	def rotate(self, dt):
		self.rotation += (PLAYER_TURN_SPEED * dt)
		
	def update(self, dt):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.rotate(-dt)
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.rotate(dt)
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			if keys[pygame.K_LSHIFT]:
				if self.booster > 0:
					self.move(dt * 2)
					self.booster -= 0.1
				else:
					self.move(dt)
			else:
				self.move(dt)
				
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.move(-dt)
		if keys[pygame.K_SPACE]:
			if self.cooldown > 0:
				pass
			else:
				self.shoot()
				
		if self.cooldown > 0:
			self.cooldown -= dt
		elif self.cooldown <= 0:
			self.cooldown = 0
			
		if self.booster_cooldown > 0:
			self.booster_cooldown -= 0.1
		elif self.booster_cooldown <= 0:
			self.booster = PLAYER_BOOSTER
			self.booster_cooldown = PLAYER_BOOSTER_COOLDOWN
			
		self.position.x = max(self.radius, min(self.position.x, SCREEN_WIDTH - self.radius))
		self.position.y = max(self.radius, min(self.position.y, SCREEN_HEIGHT - self.radius))
				
	def move(self, dt):
		unit_vector = pygame.Vector2(0, 1)
		rotated_vector = unit_vector.rotate(self.rotation)
		rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
		self.position += rotated_with_speed_vector
		
	def shoot(self):
		shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
		shot.velocity = pygame.Vector2(0, 1)
		shot.velocity = shot.velocity.rotate(self.rotation)
		shot.velocity *= PLAYER_SHOOT_SPEED
		self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

