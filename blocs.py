import pygame
from cata import Cata

class Blocs():

    def __init__(self, pos, cata):
        self.image = pygame.image.load("Assets/Images/Murs/RocBloc.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # Pour les attributs physique du joueur
        self.velocity = [3, 10]
        # Pour la catapulte des blocs
        self.cata = Cata()
        self.cata.rect.x = self.rect.x + self.rect[2] - self.cata.rect[2]
        self.cata.rect.y = self.rect.y - self.cata.rect[3]
        self.cata.pos_player = [self.cata.rect.x - self.cata.rect[2]/2, self.cata.rect.y - self.cata.rect[3]/3]
        # Pour les attributs d'états
        self.is_jumping = False
        self.is_grounded = True
        self.is_cata = cata

    def mouv(self):
        self.rect.x -= self.velocity[0]
        self.cata.rect.x -= self.velocity[0]
