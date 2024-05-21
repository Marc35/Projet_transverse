import pygame

class Canon:

    def __init__(self):
        self.image = pygame.image.load("FinalAssets/Props/canon.png")
        self.image_base = pygame.image.load("FinalAssets/Props/canon.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 720 - self.rect[3]