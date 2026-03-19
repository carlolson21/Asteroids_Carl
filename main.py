#Created by Carl Olson, March 2026.
#See GitHub for Version Control: https://github.com/carlolson21/Asteroids_Carl

#----------------------------------------------------------------------------------------
#IMPORTS
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

#----------------------------------------------------------------------------------------
#MAIN
def main():
	#SETUP
	#----------------------------------------------------------------------------------------
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	
	#High Score and Longest Time File Check
	try:
		with open("scores.json", "r") as f:
			all_games = json.load(f)
	except (FileNotFoundError, json.JSONDecodeError):
        	all_games = []
	
	#Groups
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
	
	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable)
	Shot.containers = (shots, updatable, drawable)
	
	#UI Updates
	life_display = Lives(10, 40)
	score_board = Score(10, 70)
	time_survived_display = Time_Survived(10, 10)
	boost_remaining = Boost_Time_Available(10,SCREEN_HEIGHT * 0.945)
	boost_cooldown_remaining = Boost_Cooldown_Time(10, SCREEN_HEIGHT * 0.97)
	updatable.add(life_display, score_board, time_survived_display, boost_remaining, boost_cooldown_remaining)
	drawable.add(life_display, score_board, time_survived_display, boost_remaining, boost_cooldown_remaining)
	
	#Create Player and Asteroids
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	AsteroidField()
	
	#Variables
	dt = 0
	lives = PLAYER_LIVES
	running = True
	game_over = False
	life_time = 0

	#Print to Console
	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	
	#GAME LOOP
	#----------------------------------------------------------------------------------------
	while running:
		#log state
		log_state()
		
		#Quit Loop Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
					
		#Draw Display
		screen.fill("black")
		for item in drawable:
			item.draw(screen)
		if game_over == True:
			draw_game_over_message(screen)
		pygame.display.flip()
		
		#When Alive
		if game_over == False:
		
			#Update Data
			dt = clock.tick(60) / 1000
			life_time += dt
			time_survived_display.value = f"{life_time: .2f}"
			life_display.value = lives
			boost_remaining.value = f"{player.booster:.1f}"
			boost_cooldown_remaining.value = f"{player.booster_cooldown:.1f}"
			updatable.update(dt)
			
			#Collisions
			#Loop Through Active Asteroids
			for asteroid in asteroids:
				#Player - Asteroid Collisions
				if player.collides_with(asteroid):
					log_event("player_hit")
					asteroid.kill()
					lives -= 1
					
					#When Lives = 0
					if lives <= 0:
						#Update Scoreboard
						high_scores = sorted(all_games, key=lambda x: x['score'], reverse=True)
						best_times = sorted(all_games, key=lambda x: x['time'], reverse=True)

						is_top_score = len(all_games) < 10 or score_board.value > high_scores[-1]['score']
						is_top_time = len(all_games) < 10 or life_time > best_times[-1]['time']
						
						#Add to Scoreboard if Top Ten of Either List
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
								
						#Trigger End Game Screens				    
						game_over = True
						show_leaderboard(screen, all_games)
				
				#Loop Through Active Shots	
				for shot in shots:
					#Shot - Asteroid Collisions
					if shot.collides_with(asteroid):
						log_event("asteroid_shot")
						shot.kill()
						#Score Only if Destroy, Not Split
						if asteroid.radius <= ASTEROID_MIN_RADIUS:
							score_board.value += SCORE_PER_KILL
						asteroid.split()

#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
