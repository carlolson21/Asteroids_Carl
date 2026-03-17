import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 0
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(f"Score: {self.value}", True, "white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, dt):
        self.image = self.font.render(f"Score: {self.value}", True, "white")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
