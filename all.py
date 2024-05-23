# Example file showing a circle moving on screen

import pygame
import os
from game import Game
from random import *
from math import *
pygame.init()
in_menu_run_jump = True

font = pygame.font.Font('freesansbold.ttf', 32)
screen = pygame.display.set_mode((1280, 720))

screen_w, screen_h = (screen.get_width(), screen.get_height())
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

l_skin = list_of_files("./skin", ".png")
for i, skin in enumerate(l_skin):
    l_skin[i] = pygame.image.load("./skin/"+skin).convert_alpha()
    l_skin[i] = pygame.transform.scale(l_skin[i], (50,50))
nb_skin = len(l_skin)

skin_choice = 0
#[0, 1, 2, 3,  4,  5,       6,            7,            8,    9,              10]
#[x, y, w, h, vx, vy, gravity, is_on_ground, monster_type, speed, apply_colision]
l_prop = [[-100, screen_h-40, screen_w+200, 100], [-121, -100, 100, screen_h+150], [screen_w+21, -100, 100, screen_h+150], [-100, -100, screen_w+200, 100],
          [243, 214, 349, 59], [478, 435, 382, 88], [1070, 314, 439, 75]]

#418;244;349;59 1290;352;439;75; 669;479;382;88
while in_menu_run_jump:
    keys = pygame.key.get_pressed()
    print("NB ++++", nb_skin)
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            in_menu_run_jump = False
            running = False
    
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            screen_w, screen_h = (screen.get_width(), screen.get_height())
            background_image = pygame.transform.scale(background_image, (screen_w, screen_h))
            l_prop[0], l_prop[1], l_prop[2], l_prop[3] = ([-100, screen_h-40, screen_w+200, 100], [-121, -100, 100, screen_h+150], [screen_w+21, -100, 100, screen_h+150], [-100, -100, screen_w+200, 100])
    
    if keys[pygame.K_RETURN]:
        in_menu_run_jump = False
        running = True
    
    if keys[pygame.K_LEFT] and not keys_B4["left"]:
        skin_choice = (skin_choice-1)%nb_skin
    
    if keys[pygame.K_RIGHT] and not keys_B4["right"]:
        skin_choice = (skin_choice+1)%nb_skin
    
    rect = pygame.Rect(0, 0, screen_w, screen_h)
    pygame.draw.rect(screen, "gray", rect)
    
    text = font.render("MENU RUN AND JUMP", True,(255,0,0))
    textRect = text.get_rect()
    textRect.center = (800, 200)
    screen.blit(text, textRect)

    text = font.render("APPUYER SUR ENTREE POUR JOUER", True,(255,223,0))
    textRect = text.get_rect()
    textRect.center = (800, 700)
    screen.blit(text, textRect)

    text = font.render("<| Skin précédent                        Skin suivant |>", True,(0,0,0))
    textRect = text.get_rect()
    textRect.center = (800, 540)
    screen.blit(text, textRect)
    

    screen.blit(l_skin[skin_choice], (800,525))

    pygame.display.flip()
    keys_B4 = {"z":keys[pygame.K_z], "q":keys[pygame.K_q], "s":keys[pygame.K_s], "d":keys[pygame.K_d], "space":keys[pygame.K_SPACE], "left":keys[pygame.K_LEFT], "right":keys[pygame.K_RIGHT]}
    print(l_skin[skin_choice])
class Items:
    def __init__(self, pos, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def mouv(self):
        self.rect.x -= 3

class Ennemis(Items):

    def __init__(self, pos):
        super().__init__(pos, "Assets/Images/Ennemis/pig.png")

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

class Player():

    def __init__(self):
        # Pour les attributs visuels et de positions
        self.image = l_skin[skin_choice]
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
        

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
game = Game()

# Plateformes setup
platformes = []
platformes.append(game.blocDepart)
# Graphique setup
background_0 = pygame.image.load("Assets/Images/celeste_bg.jpg")
background_0 = pygame.transform.scale(background_0, (1280, 720))
background_1 = pygame.image.load("Assets/Images/celeste_bg.jpg")
background_1 = pygame.transform.scale(background_1, (1280, 720))
play = pygame.image.load("Assets/Images/play.png").convert_alpha()
myfont = pygame.font.SysFont("monospace", 16)
# Pour les pieces
list_pieces = []
image_piece = pygame.image.load("Assets/Images/Items/piece.png")
# Pour les dashs
list_dashs = []
image_dash = pygame.image.load("Assets/Images/Items/dash.png")
image_heart = pygame.image.load("Assets/Images/heart.png")
# Pour les ennemis
list_ennemis = []
vie = 5
mort = 0
piece = 0

# Autres variables
frame_counter = 200         # Pour la gestion du temps entre le spawn des plateformes
mouseUp = False             # Pour le lancer de l'oiseau






while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and game.player.is_launching:
            mouseUp = True
        if event.type == pygame.QUIT:
            running = False

    # setup graphique
    screen.blit(background_0, (0, 0))
    screen.blit(background_1, (0, 0))
    screen.blit(game.player.image, game.player.rect)
    # Pour les pieces
    screen.blit(image_piece, (0, 0))
    score_display = myfont.render(str(game.player.piece), 1, (0, 0, 0))
    screen.blit(score_display, (8, 2))
    # Pour les dashs
    screen.blit(image_dash, (50, 0))
    score_display = myfont.render(str(game.player.nb_dash), 1, (0, 0, 0))
    screen.blit(score_display, (45, 0))
    #Pour les vies
    image_heart = pygame.transform.scale(image_heart, (40, 30))
    screen.blit(image_heart, (115, 0))
    score_display = myfont.render(str("Nombre vie : "+str(vie-mort)), 1, (0, 0, 0))
    screen.blit(score_display, (165, 2))
    font = pygame.font.Font('freesansbold.ttf', 32)
    ##### Si on est pas en phase de jeu #####
    if not game.is_playing:
        play_button = screen.blit(play, (1280/2 - play.get_size()[0]/2, 720/2 - play.get_size()[1]/2))

        if(vie-mort == 5):
            text = font.render("VOUS ALLEZ JOUER A RUN_AND_JUMP.", True,(102, 55, 38))
            screen.blit(text, (400, 460))

            text = font.render("VOUS DISPOSEZ DE 5 VIES. CHAQUE PIECE VOUS RAPPORTE 10 000 POINTS.", True,(102, 55, 38))
            screen.blit(text, (40, 500))

            text = font.render("ATTENTION, VOUS PERDEZ 2 PIECES A VOTRE TROISIEME MORT !", True,(102, 55, 38))
            screen.blit(text, (150, 540))

            pygame.display.flip()


        if(vie-mort == 0):
            running = False

        # Si le joueur clic sur le boutton play
        if play_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            game.is_playing = True

    ##### Si on est en phase de jeu #####
    if game.is_playing:

        # Permet les améliorations avec les pièces
        if game.player.piece % 15 == 0 and game.player.piece / 15 == game.player.level_dash:
            game.player.boost_dash()

        # Permet de construir les plateformes
        if frame_counter >= 200 and game.player.is_launching == False:
            frame_counter = 0
            y = randint(100, 700)
            x = 1000
            index = randint(1, 4)
            for i in range(index):
                piece = randint(0, 1)
                dash = randint(0, 5)
                ennemi = randint(0, 6)
                if i == index - 1:
                    nouv_plateforme = game.construction([x, y], True)
                else:
                    nouv_plateforme = game.construction([x, y], False)
                if piece == 1:
                    nouv_piece = game.piece_constru([nouv_plateforme.rect.x + nouv_plateforme.rect[2]/2, nouv_plateforme.rect.y - nouv_plateforme.rect[3]])
                    list_pieces.append(nouv_piece)
                if dash == 1:
                    nouv_dash = game.dash_constru([nouv_plateforme.rect.x + nouv_plateforme.rect[2]/2, nouv_plateforme.rect.y - nouv_plateforme.rect[3]])
                    list_dashs.append(nouv_dash)
                if ennemi == 1:
                    nouv_ennemi = game.ennemi_constru([nouv_plateforme.rect.x + nouv_plateforme.rect[2]/2, nouv_plateforme.rect.y])
                    nouv_ennemi.rect.y -= nouv_ennemi.rect[3]
                    list_ennemis.append(nouv_ennemi)
                x = 1000 + (i+1)*game.current_bloc.rect[2]
                platformes.append(nouv_plateforme)
        for i in platformes:                        # Build les plateformes et leurs catapultes
            screen.blit(i.image, i.rect)
            if i.rect.x < -200:
                platformes.remove(i)
            if i.is_cata != False:
                screen.blit(i.cata.image, i.cata.rect)
                if game.player.rect.colliderect(i.cata.rect) and game.player.is_flying == False:        # Permet de dectecter quand es ce que le joueur va sur une catapulte
                    game.current_bloc = i
                    game.set_sauvPoint()
                    game.current_bloc.cata.set_posPlayer()
                    game.set_lauching()
                    game.player.is_launching = True
        for i in list_pieces:
            screen.blit(i.image, i.rect)
        for i in list_dashs:
            screen.blit(i.image, i.rect)
        for i in list_ennemis:
            screen.blit(i.image, i.rect)

        # Pour le catapultage
        if game.player.is_launching:
            # Déssine le cercle de visee
            game.current_bloc.cata.set_posPlayer()
            visee = pygame.draw.circle(background_0, (255, 255, 255, 0), (game.current_bloc.cata.pos_player[0] + game.current_bloc.cata.rect[2]/2, game.current_bloc.cata.pos_player[1] + game.current_bloc.cata.rect[3]/2), 75)
            if pygame.mouse.get_pressed()[0] and visee.collidepoint(pygame.mouse.get_pos()):                # Permet la visee
                game.launching()
                pygame.draw.line(screen, "Black", (game.player.rect.x + 5, game.player.rect.y + game.player.rect[3] - 5), (game.current_bloc.cata.pos_launch_1[0], game.current_bloc.cata.pos_launch_1[1]), 5)
                pygame.draw.line(screen, "Black", (game.player.rect.x + game.player.rect[2] - 5, game.player.rect.y + game.player.rect[3] - 5),(game.current_bloc.cata.pos_launch_2[0], game.current_bloc.cata.pos_launch_2[1]), 5)
            if mouseUp and visee.collidepoint(pygame.mouse.get_pos()):       # Permet le lancé
                game.set_velocity()
                game.player.is_flying = True
                game.player.is_launching = False
                game.player.is_jumping = False
                mouseUp = False
                game.player.can_dash = True
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                game.cancel_launch()
                game.player.is_launching = False
                game.player.is_jumping = False
                mouseUp = False
            mouseUp = False

        # Quand le joueur est en vol
        if game.player.is_flying:
            game.lancer(dt)
            if pygame.key.get_pressed()[pygame.K_z] and game.player.nb_dash > 0 and game.player.can_dash:
                game.player.dash()
                game.player.can_dash = False
                game.player.nb_dash -= 1

        # Quand le joueur est sur une plateforme
        if not game.player.is_launching:

            # Pour les collisions avec le sol
            if game.player.rect.colliderect(game.blocDepart):
                game.current_bloc = game.blocDepart
            for i in platformes:
                if game.player.rect.colliderect(i):
                    game.current_bloc = i
                    game.set_sauvPoint()
            if game.current_bloc.rect.colliderect(game.player.rect):
                game.grounded()
            else:
                game.player.is_grounded = False

            # Pour le ramassage d'items
            for i in list_pieces:
                if game.player.rect.colliderect(i.rect):
                    list_pieces.remove(i)
                    game.player.piece += 1
                elif i.rect.x < -50:
                    list_pieces.remove(i)
            for i in list_dashs:
                if game.player.rect.colliderect(i.rect) and game.player.nb_dash < 3:
                    list_dashs.remove(i)
                    game.player.nb_dash += 1
                elif i.rect.x < -50:
                    list_dashs.remove(i)
            for i in list_ennemis:
                if game.player.rect.y + game.player.rect[3] <= i.rect.y + 20 and game.player.rect.colliderect(i.rect):
                    list_ennemis.remove(i)
                    game.player.piece += 3
                elif game.player.rect.colliderect(i.rect):
                    game.loose()
                    mort += 1
                    list_ennemis.remove(i)
                elif i.rect.x < -50:
                    list_ennemis.remove(i)


            if game.player.is_flying == False:
                frame_counter += 1

                # Pour les déplacements
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    game.mouv_left(dt)
                if keys[pygame.K_d]:
                    game.mouv_right(dt)
                if keys[pygame.K_SPACE] and game.player.is_jumping == False and game.player.is_grounded == True:
                    game.player.is_jumping = True
                    game.player.is_grounded = False

                # Pour le saut
                if game.player.is_jumping:
                    game.jump(dt)
                # Pour la gravité
                if game.player.is_jumping == False and game.player.is_grounded == False:
                    game.gravity(dt)

                # Pour le mouvement des plateformes et items
                for i in platformes:
                    if not (i == game.blocDepart == game.current_bloc):
                        i.mouv()
                for i in list_pieces:
                    i.mouv()
                for i in list_dashs:
                    i.mouv()
                for i in list_ennemis:
                    i.mouv()


    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    # Si le joueur perd
    if game.player.rect.y > 720 or game.player.rect.x < -50:
        if game.current_bloc.rect.x < -10:
            game.player.basic_pos = [0, 125]
        mort += 1
        game.loose()
    if game.player.vies == 0:
        game.player.piece -= 2
        game.player.vies = 3
        

    # flip() the display to put your work on screen
    pygame.display.flip()
file = open("LevelSave.txt","a")
score = game.player.piece * 3000
file.write("Score:RunJump:"+str(score)+"\n")

file.close()
pygame.quit()
