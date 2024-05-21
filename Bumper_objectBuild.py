import pygame

class ObjectBuild:

    def __init__(self, image, pos, id, force_bounce=1):
        #Image et position
        self.image = pygame.image.load(image)
        self.image_base = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.points = [[self.rect.x, self.rect.y], [self.rect.x, self.rect.y + self.rect[3]], [self.rect.x + self.rect[2], self.rect.y], [self.rect.x + self.rect[2], self.rect.y + self.rect[3]]]
        #Pour les mask hitbox
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.rect
        #Pour les collisions
        self.colli = False
        #Sauvegarder la position intiale de l'obj
        self.sauv_pos_x = pos[0]
        self.sauv_pos_y = pos[1]
        self.sauv_height = self.rect[2]
        self.sauv_width = self.rect[3]
        #Autres attrubuts
        self.bounce = force_bounce
        self.id = id
        self.angle = 0
        self.is_choosen_pos = (self.rect.x + self.rect[2]/2, self.rect.y + self.rect[3])
        #Pour les compteurs d'objets
        self.nb = 0

    def reset_visuel(self, nouv_Scale_Image=None, angle=None):
        """
        Permet de set la rotation et la taille d'un objet ainsi que sa choosen_pos
        :param nouv_Scale_Image: La nouvelle taille de l'image shouaitée (peut etre un tuple(taille_x, taille_y) ou une constante)
        :param angle: L'angle de rotation de l'objet souhaitée
        """
        if nouv_Scale_Image != None:
            if type(nouv_Scale_Image) == tuple:
                self.image = pygame.transform.scale(self.image, nouv_Scale_Image)
            else:
                self.image = pygame.transform.scale_by(self.image, nouv_Scale_Image)
        if angle != None:
            self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = self.sauv_pos_x
        self.rect.y = self.sauv_pos_y
        self.is_choosen_pos = (self.rect.x + self.rect[2] / 2, self.rect.y + self.rect[3])