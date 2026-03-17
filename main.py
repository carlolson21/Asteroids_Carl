import pygame
import sys
from constants import *
from logger import *
from player import *
from asteroid import *
from asteroidfield import *
from score import *
from gameover import *

def main():
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
	
	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable)
	Shot.containers = (shots, updatable, drawable)
	
	score_board = Score(10, 10)
	updatable.add(score_board)
	drawable.add(score_board)
	
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	AsteroidField()
	
	dt = 0
	running = True
	game_over = False

	
	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	
	while running:
		log_state()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
		screen.fill("black")
		for item in drawable:
			item.draw(screen)
		if game_over == True:
			draw_pause_message(screen)
		pygame.display.flip()
		if game_over == False:
			dt = clock.tick(60) / 1000
			updatable.update(dt)
			for asteroid in asteroids:
				if player.collides_with(asteroid):
					log_event("player_hit")
					print("Game over!")
					print(f"Score: {score_board.value}")
					game_over = True
				for shot in shots:
					if shot.collides_with(asteroid):
						log_event("asteroid_shot")
						shot.kill()
						score_board.value += 1
						asteroid.split()

if __name__ == "__main__":
    main()
