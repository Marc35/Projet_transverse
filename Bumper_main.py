import pygame
from Bumper_game import Game

game = Game()
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
# Pour le temps
clock = pygame.time.Clock()
running = True
dt = 0

# Mon setup
clic = False  # Pour les clics
press_one_key = False  # Pour pouvoir faire un seul clic de touches

font = pygame.font.SysFont('Verdana', 20, 0)  # Pour la police d'écriture

# Pour l'arrière-plan
background_00 = pygame.image.load("FinalAssets/Background/Background2/Image0.png")
game.build.mapToBuild = 0
game.build.building()
game.build_bumper.bump_classique.cpt = game.build.bump_classique.cpt
game.build_bumper.bump_speed.cpt = game.build.bump_speed.cpt
game.build_bumper.bump_gravity.cpt = game.build.bump_gravity.cpt
while running:
    with open("maps.txt", "r") as doc:
        nb_maps = len(doc.readlines())
    key = pygame.key.get_pressed()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clic = True
        if event.type == pygame.KEYDOWN:
            press_one_key = event.key

    if game.is_building:

        # Pour sortir du mode build
        if game.build.finish.rect.collidepoint(pygame.mouse.get_pos()) and clic:
            game.build_bumper.level_build = []
            game.build_bumper.bump_classique.cpt = game.build.bump_classique.cpt
            game.build_bumper.bump_speed.cpt = game.build.bump_speed.cpt
            game.build_bumper.bump_gravity.cpt = game.build.bump_gravity.cpt
            game.is_building = False
            clic = False

        # Build les items à placer
        if game.build.is_placing and clic and pygame.mouse.get_pos()[1] > 100 and pygame.mouse.get_pos()[0] < 1200:
            game.build.place(pygame.mouse.get_pos())
            clic = False

        # Modifier les items sélectionnés
        if game.build.is_mouving and game.build.is_selected != None:
            if key[pygame.K_BACKSPACE] and game.build.level_build != []:
                game.build.delete()
            if key[pygame.K_r]:
                game.build.rotate()
            if press_one_key != False and press_one_key == pygame.K_LEFT:
                press_one_key = False
                game.build.rotate(45)
            if key[pygame.K_f]:
                game.build.mouv()

        # Sélectionner les items à modifier
        for i in game.build.level_build:
            screen.blit(i.image, i.rect)
            if i.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and game.build.is_mouving:
                game.build.select(i)

        # Build les items pour choisir
        for i in range(13):
            pygame.draw.rect(screen, "black", (0 + i * 100, 0, 110, 80))
            pygame.draw.rect(screen, "grey", (0 + i * 100 + 5, 0, 100, 75))
            pygame.draw.rect(screen, "black", (1200, 0 + i * 165 - 100, 100, 165))
            pygame.draw.rect(screen, "grey", (1205, 0 + i * 165 + 5 - 100, 100, 165))
        for i in game.build.outils:
            screen.blit(i.image, i.rect)
            # Teste le cas spécial des bumpers
            if i.id == "bumper":
                screen.blit(i.plus.image, i.plus.rect)
                screen.blit(i.moins.image, i.moins.rect)
                game.build.reset_nb_bump(i)
                screen.blit(font.render(f"nb: {i.cpt}", 1, (255, 0, 0)),
                            (i.rect.x, i.rect.y + i.rect[3]))  # Compteur des bumpers
            # Pour choisir l'outil ou l'action que l'on souhaite utiliser
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.circle(screen, "green", i.is_choosen_pos, 5)
                if clic:
                    game.build.choice(i)

    if game.is_building == False:
        # Pour build la map et les bumpers
        for i in game.build.level_build:
            screen.blit(i.image, i.rect)
            if game.collision(i):
                if i.colli == False:
                    game.modifers_items(i)
                    i.colli = True
                    if i.id == "fin":
                        game.reset_ball()
                        with open("maps.txt", "r") as file:
                            nb_maps = len(file.readlines())
                        if game.build.mapToBuild < nb_maps - 1:
                            game.build.mapToBuild += 1
                            game.build.building()
                            game.build_bumper.bump_classique.cpt = game.build.bump_classique.cpt
                            game.build_bumper.bump_speed.cpt = game.build.bump_speed.cpt
                            game.build_bumper.bump_gravity.cpt = game.build.bump_gravity.cpt
                            game.build_bumper.level_build = []
                            game.isLaunched = False
                            game.isAiming = False
                            game.placing = True
                        else:
                            running = False
                            pygame.quit()
                            break
                    if i.id not in ["StopGravity_portal", "blue_portal", "red_portal", "spike", "crystal", "fin"]:
                        game.bounce(i, dt, game.collision(i))
            else:
                i.colli = False

        if running == False:
            break

        for i in game.build_bumper.level_build:
            screen.blit(i.image, i.rect)
            if game.collision(i):
                if i.colli == False:
                    game.modifiers_bumpers(i)
                    i.colli = True
                    game.bounce(i, dt, game.collision(i))
            else:
                i.colli = False
            if i.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and game.build_bumper.is_mouving:
                game.build_bumper.select(i)  # Voir quel bumper est sélectionné par le joueur

        # Pour que le joueur puisse placer des bumper
        if game.placing:

            # Pour build les outils du joueur
            for i in game.build_bumper.outils:
                screen.blit(i.image, i.rect)
                if i.id == "bumper":
                    screen.blit(font.render(f"nb: {i.cpt}", 1, (255, 0, 0)), (i.rect.x, i.rect.y + i.rect[3]))
                # Pour choisir l'outil ou l'action que l'on souhaite utiliser
                if i.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.circle(screen, "green", i.is_choosen_pos, 5)
                    if clic:
                        game.build_bumper.choice(i)
            # Pour terminer le mode placement des bumpers
            if game.build_bumper.finish.rect.collidepoint(pygame.mouse.get_pos()) and clic:
                game.placing = False
                game.isAiming = True

            # Pour placer les bumper
            if game.build_bumper.is_placing and clic and pygame.mouse.get_pos()[1] > 100:
                game.build_bumper.place_bumper(pygame.mouse.get_pos())
                game.build_bumper.reset_bumper(-1)
                clic = False

            # Pour select les bumper
            if game.build_bumper.is_mouving and game.build_bumper.is_selected != None:
                if key[pygame.K_BACKSPACE] and game.build_bumper.level_build != []:
                    game.build_bumper.delete()
                    game.build_bumper.reset_bumper(1)
                if key[pygame.K_r]:
                    game.build_bumper.rotate()
                if press_one_key != False and press_one_key == pygame.K_LEFT:
                    press_one_key = False
                    game.build_bumper.rotate(45)
                if key[pygame.K_f]:
                    game.build_bumper.mouv()

        # Pendant le lancer de la balle
        if game.isAiming:
            game.launching()
            game.set_velocity()
            if press_one_key != False and press_one_key == pygame.K_SPACE:
                game.isAiming = False
                game.isLaunched = True
                press_one_key = False
            if press_one_key != False and press_one_key == pygame.K_b:
                game.reset_ball()
                game.placing = True
                game.isAiming = False
                press_one_key = False

        if game.isLaunched:
            game.lancer(dt)
            game.gravity(dt)

            if press_one_key != False and press_one_key == pygame.K_SPACE:
                game.reset_ball()
                press_one_key = False

            if game.bullet.rect.y > 720 - game.bullet.rect[3]:
                game.bullet.rebond()

    if key[pygame.K_LSHIFT] and key[pygame.K_a]:
        game.reset_ball()
        game.placing = True
        game.isAiming = False
        press_one_key = False
        game.is_building = True

    if key[pygame.K_ESCAPE]:
        running = False
        pygame.quit()
        break

    # flip() the display to put your work on screen
    pygame.display.flip()

    # fill the screen with a color to wipe away anything from last frame
    # Pour l'arrière plan
    screen.blit(background_00, (0, 0))
    # Pour le canon et le boulet
    screen.blit(game.bullet.image, game.bullet.rect)
    screen.blit(game.canon.image, game.canon.rect)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    clic = False
    press_one_key = False

file = open("LevelSave.txt","a")
score = game.build.mapToBuild*50000
file.write("Score:RunJump:"+str(score)+"\n")
# quit pygame properly to clean up resources
pygame.quit()
