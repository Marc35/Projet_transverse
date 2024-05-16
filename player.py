import pygame
from math import *

class Player():

    def __init__(self):
        # Pour les attributs visuels et de positions
        self.image = pygame.image.load("Assets/Images/Oiseaux/normal.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.basic_pos = [0, 125]
        self.rect.x = 0
        self.rect.y = 150
        # Pour les attributs physique du joueur
        self.basic_jumpForce = 100
        self.jumpForce = 100
        self.velocity = [0, 0]
        # Pour les attributs de niveau et autres
        self.vies = 3
        self.piece = 0
        # Pour les attributs d'état de compétences
        self.can_dash = False
        self.level_dash = 1
        self.force_dash = 200
        self.nb_dash = 3
        self.planeur = None
        # Pour les attributs d'états
        self.is_jumping = False
        self.is_grounded = False
        self.is_flying = False
        self.is_launching = False

    def dash(self):
        mousePos = pygame.mouse.get_pos()
        vect_x = mousePos[0] - self.rect.x
        vect_y = mousePos[1] - self.rect.y
        norme = sqrt(vect_x**2 + vect_y**2)
        vect_x /= norme
        vect_y /= norme
        self.rect.x += vect_x * self.force_dash
        self.rect.y += vect_y * self.force_dash
        self.velocity = [0, 0]

    def boost_dash(self):
        self.force_dash += 50
        self.level_dash += 1

    def loose_pieces(self):
        self.piece -= self.piece % 15