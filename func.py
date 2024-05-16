import pygame
import math
import pymunk
import pymunk.pygame_util
import random




def clicking():  # Send True if the mouse is pressed
    return pygame.mouse.get_pressed()[0]


def mouse_event(mouse_B4):  # Give info about the state of the mouse's buttons
    """
    Return 1 at THE exact frame the mouse button is pressed
    Return -1 at THE exact frame the mouse button is unpressed
    Return 0 otherwise
    """
    # ________________Check when mouse button is clicked/realeased________________
    if mouse_B4 == False and clicking() == True:
        return 1
    elif mouse_B4 == True and clicking() == False:
        return -1
    return 0


def scalar(v1, v2):  # Return the scalar of 2 vector
    """
    Return the scalar of 2 vector
    """
    if len(v1) != len(v2):
        raise ValueError("2 vec différents lors d'un scalire est impossible")
    summ = 0
    for i in range(len(v1)):
        summ += v1[i] * v2[i]
    return summ


def norm(vector):  # Return the norm of a vector

    summ = 0
    for val in vector:
        summ += val * val
    return math.sqrt(summ)


def draw(screen, space, draw_options, bird, bird_pos, w, h, ball, ball2, ball3, font, score, background_image, cata,
         d_pig, pig, red, chuck, bomb, terence_for_show, terence, blues, matilda, king_pig, hammer, building, placing,
         building_weight):  # Draw everything for the game to render correctly
    """
    This function draw everything needed for the game

    """
    screen.blit(background_image, (0, 0))  # Place the background image
    space.debug_draw(draw_options)  # Debug options to allow pymunk to show
    screen.blit(cata, (150, 550))  # Spawn the catapulte
    if bird:
        if ball:  # If there is already a ball on screen (a rigid body so the bird azs been launched)
            # We reotate the bird acording to the body rotation,       convert radian in degre \/
            blitRotate(screen, bird, (bird_pos.x, bird_pos.y), (w / 2, h / 2), -1 * ball.body.angle * 180 / math.pi)
        else:
            # Is there is no ball we show the bird without azny roation
            blitRotate(screen, bird, (bird_pos.x, bird_pos.y), (w / 2, h / 2), 0)
        if ball2 and ball3:
            blitRotate(screen, bird, (ball2.body.position[0], ball2.body.position[1]), (w / 2, h / 2),
                       -1 * ball2.body.angle * 180 / math.pi)
            blitRotate(screen, bird, (ball3.body.position[0], ball3.body.position[1]), (w / 2, h / 2),
                       -1 * ball3.body.angle * 180 / math.pi)
        pygame.draw.line(screen, "black", (0, 0), (50, 50), 4)  # Draw a line
        pygame.draw.line(screen, "red", (50, 0), (100, 50), 4)  # Draw a line
        # Command use: pygame.draw.line(screen, "color", (x1,y1), (x2, y2), size)
        text = font.render("Score : " + str(score), True, (255, 255, 255))

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()  # GET REKT

        # set the center of the rectangular object.
        textRect.center = (1300, 20)
        screen.blit(text, textRect)
        for oink in d_pig["shape"]:
            blitRotate(screen, pig, (oink.body.position[0], oink.body.position[1]),
                       (pig.get_size()[0] / 2, pig.get_size()[1] / 2), -1 * oink.body.angle * 180 / math.pi)
        # Show the diffenrent bird on top for the user to choose from
        screen.blit(red, (150, 0))
        screen.blit(chuck, (200, 0))
        screen.blit(bomb, (300, -10))
        screen.blit(terence_for_show, (400, 0))
        screen.blit(blues, (525, 15))
        screen.blit(matilda, (600, 0))
        screen.blit(hammer, (725, 0))
        # Command use: screen.blit(image, (x,y)) the x and y of the image needs to be it's top left corner's coordinates

        # Draw lines to show the separation between the birds
        pygame.draw.line(screen, "black", (50, 0), (50, 50), 4)
        for i in range(1, 9):
            pygame.draw.line(screen, "black", (100 * i, 0), (100 * i, 50), 4)
    elif building:
        if placing:
            pygame.draw.circle(screen, "black", pygame.mouse.get_pos(), 5)
        # Draw forward and backward arrow
        pygame.draw.line(screen, "black", (0, 25), (50, 50), 4)
        pygame.draw.line(screen, "black", (0, 25), (50, 0), 4)
        pygame.draw.line(screen, "black", (450, 0), (450, 50), 4)
        pygame.draw.line(screen, "black", (550, 0), (550, 50), 4)

        pygame.draw.line(screen, "red", (50, 0), (100, 25), 4)
        pygame.draw.line(screen, "red", (50, 50), (100, 25), 4)

        pygame.draw.line(screen, "green", (125, 50), (100, 0), 4)
        pygame.draw.line(screen, "green", (125, 50), (200, 0), 4)
        pygame.draw.line(screen, "black", (50, 0), (50, 50), 4)

        pygame.draw.line(screen, "black", (200, 0), (300, 50), 4)
        pygame.draw.line(screen, "black", (200, 50), (300, 0), 4)

        pygame.draw.line(screen, "brown", (300, 25), (400, 25), 4)

        pygame.draw.line(screen, "yellow", (410, 25), (440, 25), 4)
        pygame.draw.line(screen, "yellow", (425, 10), (425, 40), 4)

        pygame.draw.line(screen, "green", (465, 25), (485, 25), 4)
        pygame.draw.line(screen, "green", (475, 15), (475, 35), 4)

        pygame.draw.line(screen, "orange", (515, 25), (535, 25), 4)

        pygame.draw.line(screen, "red", (560, 25), (590, 25), 4)

        pygame.draw.line(screen, "white", (600, 0), (700, 50), 4)

        pygame.draw.line(screen, "blue", (740, 10), (740, 40), 4)
        pygame.draw.line(screen, "blue", (760, 10), (760, 40), 4)
        text = font.render("Weight : " + str(building_weight), True, (255, 255, 255))

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()  # GET REKT

        # set the center of the rectangular object.
        textRect.center = (1300, 20)
        screen.blit(text, textRect)
        for i in range(1, 11):
            pygame.draw.line(screen, "black", (100 * i, 0), (100 * i, 50), 4)


def create_structure(space, rects):
    """
    Create all the diffenrents structure of the game
    """
    l_prop = []
    clr = [(128, 128, 128, 100), (139, 69, 19, 100)]
    # For each props, gets it position, size, color and mass
    for pos, size, color, mass in rects:
        body = pymunk.Body()  # Create a new body (by default is a dynamic body)
        body.position = pos  # Sets the position of the body to it's assigned position

        shape = pymunk.Poly.create_box(body, size,
                                       radius=5)  # Create a rectangle shape with the previoulsy created body
        # the size given and a radius to round up the edges
        shape.collision_type = 2
        shape.color = clr[color]  # Set up it's color
        shape.mass = mass  # Set up it's mass
        shape.elasticity = 0.4  # Give it an arbitrary elasticity
        shape.friction = 0.3  # Give it an arbitrary frition
        l_prop.append(shape)  # Add the shape to a list of all props
        space.add(body, shape)  # Add the newly created props to the game
    return l_prop


def map_limit(space, w=1600, h=720):
    # A list of rectangle that will be used to act as map limit
    rec = [
        [(w / 2, h - 20), (w, 40)],
        [(w / 2, 25), (w, 50)],
        [(0, h / 2), (40, h)],
        [(w, h / 2), (40, h)]
    ]
    # Similar to the previous function "create_structure", refer to it if you have question about this code
    for r in rec:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = r[0]
        body.collision_type = 2
        shape = pymunk.Poly.create_box(body, r[1])
        shape.elasticity = 0.4
        shape.friction = 0.2
        space.add(body, shape)


def add_object(space, x, y, radius, mass, c_type):
    """
    Adds an ball to the space with:
        Some coordinates
        A radius
        A mass
    """
    body = pymunk.Body(1, 1)  # Create the body
    body.position = (x, y)  # Setup it's position according to given coordinates

    shape = pymunk.Circle(body, radius)  # Creating a circle shape with the body and radius
    shape.mass = mass  # We give it the given mass
    shape.color = (0, 0, 0, 0)
    shape.collision_type = c_type
    shape.elasticity = 2 / 3  # Give an elasticity
    shape.friction = 3 / 4  # And a friction
    space.add(body, shape)  # Then adds it to the pymnuk space
    return shape


def blitRotate(screen, bird, pos, originPos, angle):
    # offset from pivot to center
    bird_rect = bird.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))  # Create a rectangle
    offset_center_to_pivot = pygame.math.Vector2(pos) - bird_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd bird center
    rotated_bird_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated bird
    rotated_bird = pygame.transform.rotate(bird, angle)
    rotated_bird_rect = rotated_bird.get_rect(center=rotated_bird_center)

    screen.blit(rotated_bird, rotated_bird_rect  )  # Show the rotated bird to the screen


def launch(v, weight, radius, space, pos, c_type):
    ball = add_object(space, pos[0], pos[1], radius, weight, c_type)  # Add the ball to the screen
    ball.body.velocity += (-10 * v[0], -10 * v[1])  # Add an impulse relative
    # to how far the bird was dragged and to the bird's weight
    return ball


def rectRect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):  # Say if 2 rectangles are touching each other
    """
    Input:
        r1x, r1y, = coordinates of the 1st rectangle
        r1w, r1h, = width and length of the 1st rectangle

        r2x, r2y, = coordinates of the 2nd rectangle
        r2w, r2h  = width and length of the 2nd rectangle
    Output:
        Bool: True => They are touching
              False =>They ain't touching

    """
    return r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y and r1y <= r2y + r2h


def gravity_formula(shape, dt, small_g=9.81, aditionnal_multiplier=100):
    # shorten lines that uses this formula
    return [aditionnal_multiplier * dt * small_g * shape.body.mass * math.sin(shape.body.angle),
            aditionnal_multiplier * dt * small_g * shape.body.mass * math.sin(shape.body.angle + math.pi / 2)]


def apply_gravity(d_prop_info, d_pig, ball, ball2, ball3, egg, dt, small_g, aditionnal_multiplier, prop_dragged):
    for prop in d_prop_info["shape"]:  # For each prop
        if prop != prop_dragged:
            g = gravity_formula(prop, dt, small_g,
                                aditionnal_multiplier)  # We calculate the gravity formula related to it
            prop.body.apply_impulse_at_local_point((g[0], g[1]),
                                                   (0, 0))  # We apply an impulse depending on that gravity formula

    # We then do the same thing for the shape and guy(pig) so evry1 gets gravity YAY !
    for shape in [ball, ball2, ball3, egg]:
        if shape:
            g = gravity_formula(shape, dt)
            shape.body.apply_impulse_at_local_point((g[0], g[1]), (0, 0))
    for guy in d_pig["shape"]:
        g = gravity_formula(guy, dt)
        guy.body.apply_impulse_at_local_point((g[0], g[1]), (0, 0))


def remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching):
    if ball:  # If there is currently a ball
        space.remove(ball, ball.body)  # We remove it
        ball = None  # We set it back to being None
        launching = False  # If there is no ball then nothing is being launched

        # We reset the birds Position
        bird_pos.x = origin_bird_pos[0]
        bird_pos.y = origin_bird_pos[1]

        # If we have a 2 other balls or if we have an egg, we remove them too
        if ball2 and ball3:
            space.remove(ball2, ball2.body)
            space.remove(ball3, ball3.body)
            ball2, ball3 = None, None
        elif egg:
            space.remove(egg, egg.body)
            egg = None
    return (ball, bird_pos, launching, ball2, ball3, egg)


def explode_prop(space, d_prop_info, explosion_center, explosion_timer, score, l_text):
    l_to_remove = []
    for prop in d_prop_info["shape"]:  # For each prop
        polygon_verticles = prop.get_vertices()  # We get all the polygons verticles
        position = prop.body.position  # We store it's position

        # We get the size of the said polygone
        length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
        width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]

        prop_image = pygame.Surface((width, length))  # We create a surface
        new_image = pygame.transform.rotate(prop_image,
                                            prop.body.angle * -180 / math.pi)  # We rotate with the right angle
        rec = new_image.get_rect()  # We get the rectangle of the image
        rec.center = position  # We set the center of the new rectangle to the old position so it stays centered
        if rectRect(explosion_center[0] - 160, explosion_center[1] - 160, 320 * (1 - explosion_timer),
                    320 * (1 - explosion_timer), rec[0], rec[1], rec[2],
                    rec[3]):  # If the explosion collides with a prop:
            # We add score
            score += 1000
            # _____We remove it_____
            space.remove(prop, prop.body)
            l_to_remove.append(prop)
            l_text.append([(prop.body.position[0], prop.body.position[1]), "1 000", (0, 0, 255), 0.8])

        l_prop_memo = d_prop_info["shape"]
        d_prop_info["shape"] = []
        for prop in l_prop_memo:
            if prop not in l_to_remove:
                d_prop_info["shape"].append(prop)
        # _________________________________________
    return (d_prop_info, score, l_text)


def rects_files(file_name, line_number):
    l_rec = []
    with open(file_name, "r") as f:
        file = f.readlines()
        for val in file[line_number % len(file)].split(";"):
            l_rec.append(val)
        f.close()
    return l_rec


def show_score_on_screens(l, dt, font, screen):
    l_to_pop = []
    for i, l_text in enumerate(l):
        text = font.render(l_text[1], True, l_text[2])
        textRect = text.get_rect()
        textRect.center = (l_text[0][0], l_text[0][1] - 70 * (2 - l_text[3]))
        screen.blit(text, textRect)
        if l[i][3] <= 0:
            l_to_pop.append(i)
        l[i][3] -= dt
    l_memo = l
    l = []
    for i, val in enumerate(l_memo):
        if i not in l_to_pop:
            l.append(val)
    return l
