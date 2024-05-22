import pygame
from pygame import Vector2

from Bumper_canon import Canon
from Bumper_bullet import Bullet
from Bumper_build import Build
from Bumper_build_bumper import Build_bumper
from math import *

class Game:

    def __init__(self):
        self.canon = Canon()
        self.bullet = Bullet(self.canon.rect.center)
        #Levels
        self.build = Build()
        self.build_bumper = Build_bumper()
        # Pour le nb de bumper par level
        self.normal_bumper = 0
        self.speed_bumper = 0
        self.gravity_bumper = 0
        #Attributs d'états
        self.isAiming = False
        self.isLaunched = False
        self.is_building = False
        self.placing = True
        # Attributs pour la physique
        self.gravité = 100

    def launching(self):
        """
        Permet de clalculer l'angle de l'aim de la balle en fonction de la position de la souris et d'orienter le canon en conséquences
        """
        angle = atan2((self.canon.rect.y + self.canon.rect[3] // 2 - pygame.mouse.get_pos()[1]), (pygame.mouse.get_pos()[0] - self.canon.rect.x - self.canon.rect[2] // 2)) * (180/pi) - 100
        center = (self.canon.rect.x + self.canon.rect[2] // 2, self.canon.rect.y + self.canon.rect[3] // 2)
        self.canon.image = pygame.transform.rotate(self.canon.image_base, angle)
        self.canon.rect = self.canon.image.get_rect(center=center)

    def set_velocity(self):
        """
        Permet de clalculer la vélocité de la balle en fonction de la position et de l'orientation du tir
        """
        pos = pygame.mouse.get_pos()
        self.bullet.velocity[0] = pos[0] - self.bullet.rect.x
        self.bullet.velocity[1] = pos[1] - self.bullet.rect.y
        norme = sqrt(self.bullet.velocity[0] ** 2 + self.bullet.velocity[1] ** 2)
        self.bullet.velocity[0] /= norme
        self.bullet.velocity[0] *= 125
        self.bullet.velocity[1] /= norme
        self.bullet.velocity[1] *= 125

    def lancer(self, dt):
        """
        Permet de calculer la trajéctoire de la balle a chaque frame en fonction du temps ainsi que de calculer la vitesse globale de la balle
        :param dt: représente le temps a chque frame (calculer dans le main par pygame)
        """
        self.bullet.rect.x += 5 * self.bullet.velocity[0] * dt
        self.bullet.rect.y += 5 * self.bullet.velocity[1] * dt
        self.bullet.vitesse = sqrt(self.bullet.velocity[0]**2 + self.bullet.velocity[1]**2)

    def gravity(self, dt):
        """
        Permet de calculer et d'appliquer la gravité
        :param dt: représente le temps a chque frame (calculer dans le main par pygame)
        """
        self.bullet.velocity[1] += dt * self.gravité

    def bounce(self, obj, dt):
        """
        Permet de calculer et d'appliquer le rebond de la balle et de set sa vélocité afin qu'elle effectue se rebond
        :param obj: l'objet qui rentre en contact avec la balle
        :param dt: représente le temps à chaque frame (calculer dans le main par pygame)
        """
        add_angle = 90      # Pour changer l'angle de la normale pour les petits bords des plateformes
        # Pousse la balle en dehors de la plateforme pour pas que la collision ne se répète
        self.bullet.rect.x -= 5 * self.bullet.velocity[0] * dt + 1
        self.bullet.rect.y -= 5 * self.bullet.velocity[1] * dt + 1

        # Pour savoir si la balle tape sur un petit coté ou un grand
        point0 = obj.points[0]
        point1 = obj.points[1]
        point2 = obj.points[2]
        point3 = obj.points[3]
        coef1 = (point0[1] - point1[1]) / (point0[0] - point1[0] + 0.0001)  # Pour les petits cotés de la planche
        coef2 = (point2[1] - point3[1]) / (point2[0] - point3[0] + 0.0001)
        origine1 = point1[1] - coef1 * point1[0]
        origine2 = point3[1] - coef2 * point3[0]
        expected_y1 = coef1 * self.bullet.rect.center[0] + origine1
        expected_y2 = coef2 * self.bullet.rect.center[0] + origine2
        if 0 < obj.angle < 180:
            # expected_y1 est la ligne du dessus, inversement pour l'autre condition
            # self.bullet.rect.y + self.bullet.rect[3] traite les edge cases (littéralement)
            if self.bullet.rect.y < expected_y2 or self.bullet.rect.y + self.bullet.rect[3] > expected_y1:
                add_angle = 0
        else:
            if self.bullet.rect.y + self.bullet.rect[3] > expected_y2 or self.bullet.rect.y < expected_y1:
                add_angle = 0

        # On calcule la normale et le rebond
        normal = [cos(radians(-(obj.angle - add_angle))), sin(radians(-(obj.angle - add_angle)))]
        vit_para = normal[0] * self.bullet.velocity[0] + normal[1] * self.bullet.velocity[1]
        self.bullet.velocity[0] -= vit_para * normal[0] + vit_para * normal[0] * obj.bounce
        self.bullet.velocity[1] -= vit_para * normal[1] + vit_para * normal[1] * obj.bounce

    def collision(self, obj):
        """
        Permet de detecter très précisément les collisions avec des masks
        :param obj: l'objet qui rentre en contact avec la balle
        """
        self.bullet.mask = pygame.mask.from_surface(self.bullet.image)
        obj.mask = pygame.mask.from_surface(obj.image)
        self.bullet.mask_rect = self.bullet.rect
        off_x = obj.rect.x - self.bullet.mask_rect.x
        off_y = obj.rect.y - self.bullet.mask_rect.y
        return self.bullet.mask.overlap(obj.mask, (off_x, off_y))

    def reset_ball(self):
        self.bullet.rect.center = self.canon.rect.center
        self.isLaunched = False
        self.isAiming = True
        self.gravité = 100

    def modifiers_bumpers(self, bumper):
        if bumper.type == "speed":
            self.bullet.velocity[0] *= 1.3
            self.bullet.velocity[1] *= 1.3
        if bumper.type == "gravity":
            self.gravité *= -1

    def modifers_items(self, item):
        if item.id == "StopGravity_portal":
            if self.gravité == 0:
                self.gravité = 100
            else:
                self.gravité = 0
        if item.id == "blue_portal":
            self.bullet.rect.x = item.red_portal.rect.center[0]
            self.bullet.rect.y = item.red_portal.rect.center[1]
        if item.id in ["spike", "crystal"]:
            self.reset_ball()
