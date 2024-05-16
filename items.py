import pygame


class Items:
    def __init__(self, pos, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def mouv(self):
        self.rect.x -= 3
