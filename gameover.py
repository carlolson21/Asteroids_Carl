import pygame
from constants import *

def draw_game_over_message(screen):
    # Create a dark transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128) # 0 is clear, 255 is solid
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0,0))

    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, "red")
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
