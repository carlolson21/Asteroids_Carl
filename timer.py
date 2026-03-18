import pygame

class Time_Survived(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 0
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(f"Time Survived: {self.value}", True, "green")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, dt):
        self.image = self.font.render(f"Time Survived: {self.value}", True, "green")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
