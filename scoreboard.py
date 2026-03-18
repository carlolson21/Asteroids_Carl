import pygame
from constants import *

def get_initials(screen):
    initials = ""
    while len(initials) < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif event.unicode.isalpha() and len(initials) < 3:
                    initials += event.unicode.upper()
        
        # Display the text on screen
        screen.fill("black")
        font = pygame.font.Font(None, 74)
        text = font.render(f"ENTER INITIALS: {initials}", True, "white")
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    return initials
    
def show_leaderboard(screen, all_games):
    # Sort for both categories
    high_scores = sorted(all_games, key=lambda x: x['score'], reverse=True)[:5]
    best_times = sorted(all_games, key=lambda x: x['time'], reverse=True)[:5]
    
    font = pygame.font.Font(None, 36)
    waiting = True
    
    while waiting:
        screen.fill("black")
        # Draw Headers
        screen.blit(font.render("TOP SCORES", True, "gold"), (100, 50))
        screen.blit(font.render("LONGEST LIFE", True, "cyan"), (450, 50))
        
        # Display Top Scores
        for i, entry in enumerate(high_scores):
            txt = f"{entry['name']}: {entry['score']}"
            screen.blit(font.render(txt, True, "white"), (100, 100 + i * 40))
            
        # Display Best Times
        for i, entry in enumerate(best_times):
            txt = f"{entry['name']}: {entry['time']}s"
            screen.blit(font.render(txt, True, "white"), (450, 100 + i * 40))

        screen.blit(font.render("Press ESC to Quit", True, "gray"), (SCREEN_WIDTH//3, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                waiting = False
