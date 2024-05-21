import pygame

class Bullet():

    def __init__(self, center):
        self.image = pygame.image.load("FinalAssets/Props/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = center[0]
        self.rect.y = center[1]
        self.velocity = [0, 0]
        self.vitesse = 0
        #Pour les masks
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.rect

    def rebond(self):
        self.rect.y -= self.rect.y - 720 + self.rect[3]
        self.velocity[1] *= -0.75
        self.velocity[0] *= 0.75