import pygame
from player import Player
from blocs import Blocs
from items import Items
from ennemis import Ennemis

class Game():

    def __init__(self):
        # Pour le joueur
        self.player = Player()
        # Pour les plateformes
        self.blocDepart = Blocs((0, 200), False)           # Pour la plateforme de départ
        self.current_bloc = self.blocDepart         # Le bloc sur lequel le joueur est actuellement
        # Pour les attributs d'états
        self.is_playing = False


    ##### Pour les actions de jeux #####
    # Pour les mouvements
    def mouv_left(self, dt):
        self.player.rect.x -= 300 * dt
    def mouv_right(self, dt):
        self.player.rect.x += 300 * dt
    def jump(self, dt):
        self.player.rect.y -= 5 * self.player.jumpForce * dt
        self.player.jumpForce -= dt * 10 * 30

    ##### Pour les forces et états #####
    # Pour la gravité
    def gravity(self, dt):
        self.player.rect.y += 10 * dt * 50

    # Pour les collisions avec le sol
    def detect_colli(self, obj, mur):
        return obj.rect.x + obj.rect[2] >= mur.rect.x and obj.rect.x <= mur.rect.x + mur.rect[2] and obj.rect.y + \
            obj.rect[3] >= mur.rect.y and obj.rect.y <= mur.rect.y + mur.rect[3]
    def grounded(self):
        """
        Réinitialise la pluparts des attributs du au fait que le joueur est au sol
        :return:
        """
        if self.player.rect.y + self.player.rect[3] - self.current_bloc.rect.y:                                     # Permet de combler si le joueur est un peut trop enfoncé dans le bloc
            self.player.rect.y -= (self.player.rect.y + self.player.rect[3] - self.current_bloc.rect.y) / 2
        self.player.is_jumping = False                             # Si il est au sol il n'est donc pas en train de sauter
        self.player.is_grounded = True                             # On met également la variable qui défini si l'oiseau est au sol sur True
        self.player.is_flying = False                              # Si il est au sol il n'est donc pas en train de voler non plus
        self.player.can_dash = False
        self.player.jumpForce = self.player.basic_jumpForce        # On réinitialise la force de saut du player pour qu'il puisse resauter
    # Pour mettre le point de sauvegarde sur le bloc courant
    def set_sauvPoint(self):
        self.player.basic_pos[0] = self.current_bloc.rect.x
        self.player.basic_pos[1] = self.current_bloc.rect.y - self.player.rect[3] - 25

    ##### Pour le lancé #####
    def set_lauching(self):
        """
        Met l'oiseau en position sur la catapulte
        """
        self.player.rect.x = self.current_bloc.cata.pos_player[0] - self.player.rect[2] / 2
        self.player.rect.y = self.current_bloc.cata.pos_player[1]
    def launching(self):
        """
        Permet au joueur de suivre la souris pour la visée
        """
        self.player.rect.x = pygame.mouse.get_pos()[0] - self.player.rect[2]/2
        self.player.rect.y = pygame.mouse.get_pos()[1] - self.player.rect[3]/2
    def set_velocity(self):
        """
        Calcule la vélocity du joueur au moment au celui lache la catapulte
        """
        self.player.velocity[0] = (self.current_bloc.cata.pos_player[0] - pygame.mouse.get_pos()[0])         # la distance en x entre la catapulte et le joueur
        self.player.velocity[1] = (self.current_bloc.cata.pos_player[1] - pygame.mouse.get_pos()[1])         # la distance en y entre la catapulte et le joueur
    def lancer(self, dt):
        """
        Calcule la trajéctoire du joueur après son lancer
        """
        self.player.rect.x += 5 * self.player.velocity[0] * dt
        self.player.rect.y += 5 * self.player.velocity[1] * dt
        self.player.velocity[1] += dt * 10 * 10
    def cancel_launch(self):
        self.player.rect.x = self.current_bloc.rect.x

    ##### Pour la constru des plateformes #####
    def construction(self, pos, cata):
        return Blocs(pos, cata)

    ##### Pour la constru des items #####
    def piece_constru(self, pos):
        return Items(pos, "Assets/Images/Items/piece.png")
    def dash_constru(self, pos):
        return Items(pos, "Assets/Images/Items/dash.png")
    def ennemi_constru(self, pos):
        return Ennemis(pos)

    ##### Si le joueur perd #####
    def loose(self):

        self.is_playing = False
        self.player.is_flying = False
        self.player.is_grounded = False
        self.player.is_launching = False
        self.player.is_jumping = False
        self.player.rect.x = self.player.basic_pos[0]
        self.player.rect.y = self.player.basic_pos[1]
        self.player.velocity = [0, 0]
        self.player.loose_pieces()
        self.player.vies -= 1
        