import pygame
import json
from constants import *
from logger import *
from player import *
from asteroid import *
from asteroidfield import *
from score import *
from gameover import *
from lives import *
from timer import *
from scoreboard import *

def main():
	#SETUP
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	
	try:
		with open("scores.json", "r") as f:
			all_games = json.load(f)
	except (FileNotFoundError, json.JSONDecodeError):
        	all_games = []

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
	
	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable)
	Shot.containers = (shots, updatable, drawable)
	
	life_display = Lives(10, 40)
	score_board = Score(10, 70)
	time_survived_display = Time_Survived(10, 10)
	updatable.add(life_display, score_board, time_survived_display)
	drawable.add(life_display, score_board, time_survived_display )
	
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	AsteroidField()
	
	dt = 0
	lives = PLAYER_LIVES
	running = True
	game_over = False
	life_time = 0

	
	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	
	#GAME LOOP
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
			draw_game_over_message(screen)
		pygame.display.flip()
		if game_over == False:
			dt = clock.tick(60) / 1000
			life_time += dt
			time_survived_display.value = f"{life_time: .2f}"
			life_display.value = lives
			updatable.update(dt)
			for asteroid in asteroids:
				if player.collides_with(asteroid):
					log_event("player_hit")
					asteroid.kill()
					lives -= 1
					if lives <= 0:
						high_scores = sorted(all_games, key=lambda x: x['score'], reverse=True)
						best_times = sorted(all_games, key=lambda x: x['time'], reverse=True)

						is_top_score = len(all_games) < 10 or score_board.value > high_scores[-1]['score']
						is_top_time = len(all_games) < 10 or life_time > best_times[-1]['time']

						if is_top_score or is_top_time:							
							name = get_initials(screen)
							result = {
								"name": name,
								"score": score_board.value,
								"time": round(life_time, 2)
							}
							all_games.append(result)
							all_games = sorted(all_games, key=lambda x: x['score'], reverse=True)[:20]
							with open("scores.json", "w") as f:
								json.dump(all_games, f)					    
						game_over = True
						show_leaderboard(screen, all_games)
				for shot in shots:
					if shot.collides_with(asteroid):
						log_event("asteroid_shot")
						shot.kill()
						if asteroid.radius <= ASTEROID_MIN_RADIUS:
							score_board.value += SCORE_PER_KILL
						asteroid.split()


if __name__ == "__main__":
    main()
