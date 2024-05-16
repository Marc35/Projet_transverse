import pygame

class Cata():

    def __init__(self):
        self.image = pygame.image.load("Assets/Images/catapulte.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], self.image.get_size()[1]*1.5))
        self.rect = self.image.get_rect()
        self.pos_player = [self.rect.x + self.rect[2]/2, self.rect.y]            # La position du joueur quand il ira dans la catapulte
        self.pos_launch_1 = [self.rect.x + 5, self.rect.y + 20]
        self.pos_launch_2 = [self.rect.x + self.rect[2] - 5, self.rect.y + 20]

    def set_posPlayer(self):
        self.pos_player = [self.rect.x + self.rect[2]/2, self.rect.y]
        self.pos_launch_1 = [self.rect.x + 5, self.rect.y + 20]
        self.pos_launch_2 = [self.rect.x + self.rect[2] - 5, self.rect.y + 20]