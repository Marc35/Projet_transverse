# Import
import pygame
import math
import pymunk
import pymunk.pygame_util
import random
from func import *



# _____pygame setup_____
pygame.init()
screen = pygame.display.set_mode((1600, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Les oiseaux pas très content")

#______________________________ Variable initialisation______________________________
running = True

birds_status = 1
#1 : red
#2 : chuck
#3 : bomb
#4 : terence
#5 : the blues
#6 : matilda

create_white_dot = True
l_white_dot=[]
explosion_center = (0,0)
explosion_timer =0
building_weight = 50
first_po_prop = None
dragging = False
launching = False
building = False
velocity = [0,0]
friction_factor = 2/3 
small_g = 9.81
l_rec = []
prop_dragged = None
dt = 0
bird_pos = pygame.Vector2(144, 547)
origin_bird_pos = (144,547)
white = (255, 255, 255)
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
radius = 20
ball = None
ball2, ball3 = None, None
paused = False
egg = None
capacity = False
mouse_B4 = False
placing = False
c_pressed = 0
weight = 10
frame_counter = 0
line_number = 0
gravity_multiplier = 100
l_timer_destruction = []
l_text = []
d_prop_info = {
    "shape": [],
    "last_vel": [],
    "hp": [],
    "material": []
}

d_pig = {
    "shape": [],
    "last_vel": []

}
file_name = "map.txt"

#d_prop_info["shape"] = prop shape (pymunk stuff)
#d_prop_info["last_vel"] = velocity of last frame (used to calculate the difference in velocity to calculate if a structures breaks or not)
#d_prop_info["hp"] = health of a prop
d_prop_info["last_vel"] = []

#________ Charge les images pour le jeu ________
#name_image = pygame.image.load('image.extension').convert_alpha() <- convert alpha makes images use much faster
#name_image = pygame.transform.scale_by(name_image, factor by which we multiply the size of the image)

red = pygame.image.load('red.png').convert_alpha()
red = pygame.transform.scale_by(red, 0.04)

chuck = pygame.image.load('chuck.png').convert_alpha()
chuck = pygame.transform.scale_by(chuck, 0.04)

bomb = pygame.image.load('bomb.png').convert_alpha()
bomb = pygame.transform.scale_by(bomb, 0.06)

terence_for_show = pygame.image.load('terence.png').convert_alpha()
terence_for_show = pygame.transform.scale_by(terence_for_show, 0.05)

terence = pygame.image.load('terence.png').convert_alpha()
terence = pygame.transform.scale_by(terence, 0.1)

blues = pygame.image.load('blues.png').convert_alpha()
blues = pygame.transform.scale_by(blues, 0.05)

matilda = pygame.image.load('matilda.png').convert_alpha()
matilda = pygame.transform.scale_by(matilda, 0.09)

king_pig = pygame.image.load('king_pig.png').convert_alpha()
king_pig = pygame.transform.scale_by(king_pig, 0.04)

pig = pygame.image.load('pig.png').convert_alpha()
pig = pygame.transform.scale_by(pig, 0.04)

hammer = pygame.image.load('hammer.png').convert_alpha()
hammer = pygame.transform.scale_by(hammer, 0.09)

bird = red

w, h = bird.get_size() #We get height and width of the current bird (red)

cata = pygame.image.load("catapult.png").convert_alpha()
cata = pygame.transform.scale_by(cata, 0.25)

background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (1600, 870)) 
#________________________________________________________________________





space = pymunk.Space() #Generate the pymunk space
space.gravity = (0, 0) #Sets its gravity to 0,0 so we calculate it manually
draw_options = pymunk.pygame_util.DrawOptions(screen) #Give the pygame screen to pymunk
#_____________________________Functions________________________________


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



#______________________________Setting up variables______________________________
save = rects_files(file_name, line_number)
rects = []

for i in range(int(len(save)/6)): #In the save, each rectangles has 6 parameters so we divid by 6 to get the nb of rect
    if save[0+i*6] == "pig":
        d_pig["shape"].append(add_object(space, int(save[1+i*6]), int(save[2+i*6]), 30, 10, 2))
    else:
        rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
    #We add a rectangle,[(x, y), (w,h), color, mass]

#Place the props and note all of them in a list inside a dict
d_prop_info["shape"] = create_structure(space, rects)

for prop in d_prop_info["shape"]: #We itteratte for each prop: 
    #We note it's last velocity
    d_prop_info["last_vel"].append(prop.body.kinetic_energy)

#Create the limit of the map
map_limit(space)


with open(file_name, "r") as f:
    lines = f.readlines()
    nb_level = len(lines)
    f.close()

while running: #We loop while the game is running
    
    nb_pig = len(d_pig["shape"]) #We note the number of pig

    if nb_pig == 0 and not building: #If there is no pig left
        if nb_level == line_number: #If we are at the last level
            running = False
            print("You won !") #You won
        else:
            #We remove all body on the screen
            #And reset variables to be able to launch again
            ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
            capacity = False
            create_white_dot = True
            l_white_dot = []
            rects = []
            for guy in d_pig["shape"]:
                space.remove(guy, guy.body)
            d_pig["shape"] = []
            d_pig["last_vel"] = []
            line_number+=1 #Take the next line numer
            save = rects_files(file_name, line_number) #Get the save from the save file
            for i in range(int(len(save)/6)):  #For each prop in the save file
                #We place it in a list
                if save[0+i*6] == "pig":
                    d_pig["shape"].append(add_object(space, int(save[1+i*6]), int(save[2+i*6]), 30, 10, 2))
                else:
                    rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
            
            #We clear every current shape from the sapce
            for props in d_prop_info["shape"]:
                space.remove(props, props.body)
            
            #We put all new shape in the list that keep tracks of props 
            #And we add them to the space at the same time
            d_prop_info["shape"] = create_structure(space, rects)


    
    keys = pygame.key.get_pressed()#We get the current status of all keybord key

        

    for event in pygame.event.get():#We check the pygame event
        if event.type == pygame.QUIT: #If the user click the X
            running = False #We stop the loop
    
    #We apply the gravity to everything
    apply_gravity(d_prop_info, d_pig,ball, ball2, ball3, egg ,dt, small_g, gravity_multiplier ,prop_dragged)

    #We check if the pig as been "killed"
    l_to_remove = []
    for guy, last_vel in zip(d_pig["shape"], d_pig["last_vel"]): #For each pig
        
        #If the difference in velocity between 2 frames is to huge compare to it's mass (a heavier pig would need a more brutal shock)
        if abs(guy.body.kinetic_energy-last_vel) > 100000*guy.body.mass and not building: 
            
            #We remove the pig
            space.remove(guy, guy.body) #We remove it from the space
            l_to_remove.append(guy) #We will remove it from the list of current pig

            #We add the its position and other info to a list to show a cool effect to the score
            l_text.append([(guy.body.position[0], guy.body.position[1]), "10 000", (255,223,0), 2]) 
            score += 10000
        
        #We clear the list of shape and rebuild it without "dead" pig
        l_pig_memo = d_pig["shape"]
        d_pig["shape"] = []

        #For each pig in the game
        for piggy in l_pig_memo: 
            if piggy not in l_to_remove: #If we don't want to remove it
                d_pig["shape"].append(piggy) #We had him back to the list
    
    #pygame.draw.rect(screen, "black", pygame.Rect(bird_pos.x, bird_pos.y, round((1-explosion_timer)*3200), round((1-explosion_timer)*3200)))
    
    #We check if prop should be destroyed
    l_to_remove = []
    for prop, last_vel in zip(d_prop_info["shape"], d_prop_info["last_vel"]):#For each prop
        
        #If the difference in velocity between 2 frames is to huge compare to it's mass (a heavier prop would need a more brutal shock)
        if abs(prop.body.kinetic_energy-last_vel) > 50000*prop.body.mass and not building:
            
            #We remove the prop from the game
            space.remove(prop, prop.body)#We remove it from the pymunk space
            l_to_remove.append(prop) #We will remove it after the end of this loop
            l_timer_destruction.append([prop, 1]) #We add it to a list to make cool particles affect

            #We add the its position and other info to a list to show a cool effect to the score
            l_text.append([(prop.body.position[0], prop.body.position[1]), "1 000", (0,0,255), 0.8])
    
            score += 1000
        
        #We clear the list of shape and rebuild it without destroyed prop
        l_prop_memo = d_prop_info["shape"]
        d_prop_info["shape"] = []
        
        for prop in l_prop_memo: #For each prop
            if prop not in l_to_remove: #If the prop hasn't been destroyed
                d_prop_info["shape"].append(prop) # We add it back to the list
            
    event = mouse_event(mouse_B4) #get mouse event (check if mouse just got pressed/unpressed)

    l_text = show_score_on_screens(l_text, dt, font, screen) # We show the text needed on screen

    if event == 1: #If mouse just got pressed
        
        #If the mouse clicked on the bird while we aren't launching and the bird is on the screen (Not building)
        if abs(pygame.mouse.get_pos()[0]-bird_pos.x) < 30 and abs(pygame.mouse.get_pos()[1]-bird_pos.y) < 30 and not launching and bird:
           
            #It means we are dragging around the bird
            dragging = True
           
            #We note the coordinates to calculate how far the mouse moved
            origin_coo = pygame.mouse.get_pos()

        #If the mouse clicked in the top 50 pixels of the screen (Tool bar) and a bird is on the screen
        if pygame.mouse.get_pos()[1] < 50 and bird:
            """
            In this section we will to what's asked by the user
            Since to enter this if statement ths user has clicked in the top 50 pixels,
            We won't need to check the y coordinates of the mouse, only the x coordinates will need to be checked
            1st = Bring the bird to the catapult
            2nd = Rebuild the current structure
            3rd to 8th = List of bird
            9th = Building mode
            """

            #1 bring bird to cata
            if pygame.mouse.get_pos()[0] < 50:
                #We clear the game from any ball, and put it back on the cata (see remove_ball for more info)
                ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
                #We give back the ability to use a special capacity
                capacity = False
                create_white_dot = True
            
            #2 Rebuild structure
            elif 50<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 100:
                #We destroy then rebuild evrything
                for props in d_prop_info["shape"]:#For each prop
                    space.remove(props, props.body)#We remove it from the space
                d_prop_info["shape"] = create_structure(space, rects) #We rebuild all props

            #________ List of all bird________
                """
            To change the bird, the code is the same way for each bird:
            bird  = new_bird
            birds_status = new_status (used for special capacity)
            weight = new_weight
            radius = new_bird_radius
            w,h = bird.get_size() #Set up the right size for the image used in some calculation
            """
            elif 100<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 200 and not launching:
                #1st bird : Red (The original)
                bird = red
                birds_status = 1
                weight = 10
                radius = 20
                w, h = bird.get_size()
            elif 200<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 300 and not launching:
                #2nd bird : Chuck (The yellow one with a dash)
                bird = chuck
                birds_status = 2
                weight = 17
                radius = 20
                w, h = bird.get_size()
            elif 300<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 400 and not launching:
                #4rd bird : Bomb (The black explosive one)   
                bird = bomb
                birds_status = 3
                weight = 25
                radius = 25
                w, h = bird.get_size()
            elif 400<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 500 and not launching:
                #5th bird : Terence (The big red one, no capacity except being overweight)
                bird = terence
                birds_status = 4
                weight = 100
                radius = 35
                w, h = bird.get_size()
            elif 500<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 600 and not launching:
                #6th bird : Blues (The blue one that divide into three 3 blue birds (They are brothers named Jay, Jake and Jim))
                bird = blues
                birds_status = 5
                weight = 6
                radius = 13
                w, h = bird.get_size()
            elif 600<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 700 and not launching:
                #7th bird : Matilda (The white one that shoots a egg to the ground)
                bird = matilda
                birds_status = 6
                weight = 20
                radius = 25
                w, h = bird.get_size()
            #________End list of bird________
            
            #9 Building mode
            elif 700<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 800 and not launching:
                bird = hammer #We swape the bird to the hammer
                birds_status = -1 #The status is changed to -1 to prevent capacity or other bug
                bird = None #We remove the bird
                building = True #We set ourselves in building mode
        
        #If the mouse clicked on the tool bar while we are in building mode
        elif pygame.mouse.get_pos()[1] < 50 and building:
            """
            This is a list of all possible action in the tool bar
            While being in the buiding mode

            """
            
            #Previous preset
            #This will clear the map and load the n-1 preset
            if pygame.mouse.get_pos()[0] < 50:
                rects = []
                for guy in d_pig["shape"]:
                    space.remove(guy, guy.body)
                d_pig["shape"] = []
                d_pig["last_vel"] = []
                line_number-=1 #Take the previous line numer
                save = rects_files(file_name, line_number) #Get the save from the save file

                for i in range(int(len(save)/6)): #For each prop in the save file
                    #We place it up in a list
                    if save[0+i*6] == "pig":
                        d_pig["shape"].append(add_object(space, int(save[1+i*6]), int(save[2+i*6]), 30, 10, 2))
                    else:
                        rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
                
                #We clear every current shape from the sapce
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                
                #We put all new shape in the list that keep tracks of props 
                #And we add them to the space at the same time
                d_prop_info["shape"] = create_structure(space, rects)
            
            #Next preset
            #This will clear the map and load the n+1 preset
            elif 50<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 100:
                rects = []
                for guy in d_pig["shape"]:
                    space.remove(guy, guy.body)
                d_pig["shape"] = []
                d_pig["last_vel"] = []
                line_number+=1 #Take the next line numer
                save = rects_files(file_name, line_number) #Get the save from the save file
                for i in range(int(len(save)/6)):  #For each prop in the save file
                    #We place it in a list
                    if save[0+i*6] == "pig":
                        d_pig["shape"].append(add_object(space, int(save[1+i*6]), int(save[2+i*6]), 30, 10, 2))
                    else:
                        rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
                
                #We clear every current shape from the sapce
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                
                #We put all new shape in the list that keep tracks of props 
                #And we add them to the space at the same time
                d_prop_info["shape"] = create_structure(space, rects)
            
            #Re launch the game
            #This will quit the building mode, restore all parameters to be ready to play
            elif 100<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 200:
                #We initialize all variables back to being able to play normally
                building = False
                placing = False
                first_po_prop = None
                prop_dragged = None
                paused = False
                l_white_dot = [] 
                small_g = 9.81
                bird = red
                birds_status = 1
                weight = 10
                radius = 20
                w, h = bird.get_size()
            
            #Instant clear
            #We instantly clears the map from any props
            elif 200<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 300:
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                d_prop_info["shape"] = []
                for guy in d_pig["shape"]:
                    space.remove(guy, guy.body)
                d_pig["shape"] = []

            
            #Placing mode
            #This puts the user in placing mode
            #A black dot will be on the cursor of the user to indicate that he is in placing mode
            elif 300<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 400:
                #Depending on whether the user was already in placing mode or not
                #We change the mode to be placing / not longer placing
                if not placing: 
                    placing = True
                    first_po_prop = None
                else:
                    placing = False
                    first_po_prop = None
            
                """
                While in placing mode, the weight of the the structure matter so to change it
                There is 4 buttons to add restictively from left to right:
                50, 5, -5, -50
                Made for user to adjust the weight without having to spam a +1 a hundred times
                """
           
           # Adds 50 weight
            elif 400<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 450:
                building_weight += 50
            
            # Adds 5 weight
            elif 450<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 500:
                building_weight +=5
            
            # Remove 5 weight
            elif 500<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 550:
                #We check if the weight is strictly superior to 5 so the weight doesn't get negative
                if building_weight > 5:
                    building_weight -=5
            
            # Remove 50 weight
            elif 550<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 600:
                #Same thing than for the -5 button
                #We check if the weight is strictly superior to 50 so the weight doesn't get negative
                if building_weight > 50:
                    building_weight -=50
            
            #Save
            #We get the position of all props in the game and store them in a text file
            elif 600<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 700:
                rects = []
                line= ""
            
                #For each prop
                for prop in d_prop_info["shape"]:
                    polygon_verticles = prop.get_vertices() #We get all the polygons verticles
                    position = prop.body.position #We store it's position
                    mass = prop.body.mass
                    #We get the size of the said polygone
                    width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]
                    length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
                    
                    rects.append([position, (width, length), 0, mass])
                for rec in rects:
                    #We add all of the props caracteristics to the line
                    #We do so for eac prop
                    line += str(round(rec[0][0]))+";"+str(round(rec[0][1]))+";"+str(round(rec[1][0]))+";"+str(round(rec[1][1]))+";"+str(round(rec[2]))+";"+str(round(rec[3]))+";"
                
                #We add the pig to the line
                for oink in d_pig["shape"]:
                    line += "pig;"+str(round(oink.body.position[0]))+";"+str(round(oink.body.position[1]))+";0;0;0;"
                #Finally we write the line
                with open(file_name, "a") as f:
                    f.write(line+"\n")
                    f.close()
            
            #Pause
            #We stop the game from calculating gravity, mouvement, rotation etc..
            elif 700<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 800:
                if paused:
                    paused = False
                    small_g = 9.81
                else:
                    paused = True
        
        #If we are in placing mode
        elif placing:
            #If we've already placed a point
            if first_po_prop:
                #We get the size of the prop depending on how far is the click for the first placed point 
                #(We set the distance to 1 if it's 0 to prevent bug while placing the block)
                size = (pygame.mouse.get_pos()[0]-first_po_prop[0] if pygame.mouse.get_pos()[0]-first_po_prop[0]!=0 else 1,
                        pygame.mouse.get_pos()[1]-first_po_prop[1] if pygame.mouse.get_pos()[1]-first_po_prop[1]!=0 else 1)

                #We add the new structures to the list of structure while creating it on the space
                d_prop_info["shape"]+=create_structure(space, [[(first_po_prop[0]+size[0]/2, first_po_prop[1]+size[1]/2),size , 0, building_weight]])
                first_po_prop = None
                l_white_dot = []
            else:
                #If it's the first click we get the clicked_position
                first_po_prop = pygame.mouse.get_pos()
                #We add a point on the screen where the mouse was clicked
                l_white_dot.append((screen, "black", first_po_prop, 10))
        
        #If we are in the building mode without being in placing mode
        elif building and not placing: #The "and not placing" is useless but it's to be clear
            """
            This function will help the user to select a given prop
            He will then be able to perform action on it such as rotating it
            Moving it to follow the mouse
            Copy it or delete it
            """
            #If we clicked while dragging a prop, we are no longer dragging it
            if prop_dragged:
                prop_dragged = None

            #If we aren't already dragging a prop
            else:
                #We check the collision for each prop, if we are touching one
                #We set it as the prop we are dragging
                for prop in d_prop_info["shape"]:
                    polygon_verticles = prop.get_vertices() #We get all the polygons verticles
                    position = prop.body.position #We store it's position
                    
                    #We get the size of the said polygone
                    length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
                    width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]

                    prop_image = pygame.Surface((width, length)) #We create a surface
                    new_image = pygame.transform.rotate(prop_image, prop.body.angle*-180/math.pi) #We rotate with the right angle
                    rec = new_image.get_rect() #We get the rectangle of the image
                    rec.center = position #We set the center of the new rectangle to the old position so it stays centered
                    if rectRect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, rec[0], rec[1], rec[2], rec[3]):
                        prop_dragged = prop

        #If the bird is being launched and we hav'nt used it's special ability
        elif launching and not capacity:
            """
            For each status of bird, we apply different ability
            """
            #Chuck
            #The Yellow One
            if birds_status == 2:
                capacity = True
                #We give a boost in speed forward
                print(ball.body.velocity)
                ball.body.apply_impulse_at_local_point((25000,0),(0,0))
            
            #Bomb
            #The Black One
            elif birds_status == 3:
                capacity = True
                #We give him a giantic boost so he glitch out of the screen but we don't remove him to prevent having bugs
                ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))

                #We set up variable for the explosion to work properly
                explosion_timer = 1
                explosion_center = (bird_pos.x, bird_pos.y)

                #We call the explosion function
                d_prop_info, score,l_text = explode_prop(space, d_prop_info, explosion_center, explosion_timer, score, l_text)
            
            #The blues
            #The little blue one
            elif birds_status == 5:
                capacity = True
                #We create 2 more birds with a boost slightly downward and upward
                velocity2 = [velocity[0], velocity[1]*4/3+15]
                ball2 = launch(velocity2, weight, radius, space, ball.body.position, 0)
                velocity3 = [velocity[0], velocity[1]*1/4-15]
                ball3 = launch(velocity3, weight, radius, space, ball.body.position, 0)
            
            #Matilda
            #The White One
            elif birds_status == 6:
                capacity = True

                #We summon an egg that comes slamming down into the ground
                velocity_egg = [velocity[0], velocity[1]]
                egg = launch(velocity_egg, weight, radius, space, ball.body.position, 0)
                egg.body.apply_impulse_at_local_point((velocity[0], 88000),(0,0))#Add an impulse relative 
                ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))
    
    elif event == -1: #If mouse just got unpressed
        if dragging: #If the user was dragging the bird from the cata
            #We launch it
            dragging = False
            launching = True
            l_white_dot = []
            #The velocity applied is the distance dragged from origin point were the mouse was clicked
            velocity = [(bird_pos.x-origin_coo[0]), (bird_pos.y-origin_coo[1])]

            #If there is already a ball(reminder, ball = body) we remove it
            ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
                
            #Finally we launch the bird
            #Given the velocity calculated up above
            ball = launch(velocity, weight, radius, space, bird_pos, 1)


    if prop_dragged: #If the user has selected a prop
        #We move to props to stay under the cursor
        prop_dragged.body.position = pygame.mouse.get_pos()

        #We draw a white cirlce on the selected to prop to show the user clearly which prop has been selected
        #And to clarify IF a prop has been selected
        pygame.draw.circle(screen, "white", prop_dragged.body.position, 10)

        if keys[pygame.K_c]:
            if c_pressed == 0:
                c_pressed = 1
            else:
                c_pressed = -1
        else:
            c_pressed = 0

        #If we pres a or e we rotate the prop
        if keys[pygame.K_e]:
            prop_dragged.body.angle +=2*dt
        elif keys[pygame.K_a]:
            prop_dragged.body.angle -=2*dt
        
        #If we press d we delete the prop from the game
        elif keys[pygame.K_d]:
            #We remove it from the space
            space.remove(prop_dragged, prop_dragged.body)
            d_memo = d_prop_info["shape"]
            d_prop_info["shape"] = []
            #We remove it from the list of props
            for prop in d_memo:
                if prop != prop_dragged:
                    d_prop_info["shape"].append(prop)
            #We are no longer dragging anything
            prop_dragged = None
        
        #If we pressed c we duplicate the current prop
        elif c_pressed == 1:
            polygon_verticles = prop_dragged.get_vertices() #We get all the polygons verticles
            position = prop_dragged.body.position #We store it's position        
            #We get the size of the said polygone
            width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]
            length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
            
            #We create another prop with the same parameter as the selected one
            d_prop_info["shape"]+=create_structure(space, [[prop_dragged.body.position,(width, length) , 0, prop.body.mass]])

    if explosion_timer > 0: #If there is an explosion on going
        #We explode the prop according to the explosion's center, it's evolution
        #And update the prop list according to it
        d_prop_info, score, l_text = explode_prop(space, d_prop_info, explosion_center, explosion_timer, score, l_text)

        #We draw 350 points
        for i in range(350):
            #We get a random position for the center point
            explo_co = [random.randint(-500, 500), random.randint(-500, 500)]

            #We get the invers of the norm to stay propotionnal
            if explo_co != [0, 0]:
                k = 1/norm(explo_co)
            else:
                k= 1

            #The minimum distance between the point and the explosion wave
            distance_min = round((1-explosion_timer)*160)-30

            #If it's negative we set it to 0
            if distance_min<0:
                distance_min=0
            
            #The distance is therfore choosen randomly between the minimum distance and
            #A value time 160 that increase as the timer decrease reaching eventually close to 160
            distance = random.randint(distance_min, round((1-explosion_timer)*160))
            #distance = random.randint(0, round((1-explosion_timer)*160))
            #This is an alternative without the wave effect   /\
            #                                                 ||

            #We multiply the random value by the inverse of the norm to keep it proportinnal 
            #Which give us a random direction
            #We then multiply by the previously caluclated distance
            explo_co[0] *= k*distance
            explo_co[1] *= k*distance

            #We place the point relatively to the center of the explosion
            explo_co[0] += explosion_center[0]
            explo_co[1] += explosion_center[1]

            #We draw it in a random color at the given place
            pygame.draw.circle(screen, random.choice(["grey", "red", "red", "red", "orange", "orange"]), (explo_co[0], explo_co[1]), 5)
        #We decrease the timer by dt (times 4 to speed things up but it's open to being changed)
        explosion_timer -= dt*4
    
    for i in range(len(l_timer_destruction)): #If a prop as been destroyed, for each destryoed prop
        #while the timer is postive
        if l_timer_destruction[i][1] > 0:
            #We draw 45 points colored randomly to show a destruction effect
            for j in range(45):
                pygame.draw.circle(screen, random.choice(["white", "white", "white", "gray", "gray", "black"]), (l_timer_destruction[i][0].body.position[0]+random.randint(-100, 100), l_timer_destruction[i][0].body.position[1]+random.randint(-100, 100)), 5)
        l_timer_destruction[i][1] -= dt*5
    
    if keys[pygame.K_r] and bird:#If we press R key we reset bird's position
        #We remove all body on the screen
        #And reset variables to be able to launch again
        ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
        capacity = False
        create_white_dot = True
        l_white_dot = []

    if keys[pygame.K_p] and not last_key and building: #Place a pig
        #We add a pig to the game
        d_pig["shape"].append(add_object(space, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 30, 10, 2))

    if dragging: #While we're dragging the bird:

        #We adjust the bird's postion for it stay under the mouse but not to teleport if the bird's wasn't clicked in it's center
        move_x = pygame.mouse.get_pos()[0] - origin_coo[0]
        move_y = pygame.mouse.get_pos()[1] - origin_coo[1]
        while (norm((move_x,move_y))>140):
            move_x *=0.99
            move_y *=0.99
        bird_pos.x = origin_bird_pos[0] + move_x
        bird_pos.y = origin_bird_pos[1] + move_y

        #We draw the rubber band of the stone launcher
        pygame.draw.line(screen, "black", (bird_pos.x-w/2, bird_pos.y+5), (165, 565), 4)
        pygame.draw.line(screen, "black", (bird_pos.x+w/2, bird_pos.y+15), (190, 565), 4)
        #pygame.draw.line(screen, "black", (bird_pos.x+5, bird_pos.y+5), (bird_pos.x-25, bird_pos.y-5), 3)
    
    
    if paused: #If the user pressed the pause button in building mode
        #We stop the gravity to prevent evrything from going downward velocity
        small_g = 0

        #For each prop
        for prop in d_prop_info["shape"]:
            #We set their velocity to 0 to prevent them from moving
            prop.body.velocity = (0,0)
            #We set their angular velocity to 0 to prevent them from rotating
            prop.body.angular_velocity = 0
        #Same thing for each pig
        for guy in d_pig["shape"]:
            #We set their velocity to 0
            guy.body.velocity = (0,0)
            #And also set their angular velocity to 0
            guy.body.angular_velocity = 0

    for dot in l_white_dot: #For each dot we want to draw
        #We draw it to the asked position with the asked color and radius
        pygame.draw.circle(dot[0], dot[1], dot[2], dot[3])
    
    d_pig["last_vel"] = []
    for guy in d_pig["shape"]: #For each pig we note it's last velocity 
        #It's used to calculate the difference of velocity and in the end, calculate if the pig should "die"
        d_pig["last_vel"].append(guy.body.kinetic_energy)
    
    
    d_prop_info["last_vel"] = []
    for prop in d_prop_info["shape"]: #For each prop
        if ball: #If a body exist
            polygon_verticles = prop.get_vertices() #We get all the polygons verticles
            position = prop.body.position #We store it's position
                        
            #We get the size of the said polygone
            length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
            width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]

            prop_image = pygame.Surface((width, length)) #We create a surface
            new_image = pygame.transform.rotate(prop_image, prop.body.angle*-180/math.pi) #We rotate with the right angle
            rec = new_image.get_rect() #We get the rectangle of the image
            rec.center = position #We set the center of the new rectangle to the old position so it stays centered

            #If the bird is hitting a prop
            if rectRect(ball.body.position[0]-radius, ball.body.position[1]-radius, radius*2+10, radius*2+10,rec[0], rec[1], rec[2], rec[3]):
                #We stop placing dots
                create_white_dot = False
                #Execpt if it's Bomb we stop it from using his capacity
                #Why is bomb exempted ? Bcs it's funny and i like it so be it
                if birds_status !=3:
                    capacity = True
        #We note the lastest velocity of the prop to calc if it will be destroyed
        d_prop_info["last_vel"].append(prop.body.kinetic_energy)
    

    #We remember the status of the mouse for the next when we will use mouse_event()
    mouse_B4 = clicking()

    #Display the game on the screen
    pygame.display.flip()

    #limits FPS to 60
    #dt is delta time in seconds since last frame used in multiple operation
    #It's the time between each frame
    dt = clock.tick(60) / 1000
    #We cap dt so it's doesn't give a huge value if it freezes
    #Or when you drag the pygame window the game stop calculating but dt ain't stopping
    if dt > 1/30:
        dt = 1/30

    space.step(dt) #We advance the simulation by dt so it stays logical even in case of higher/lower fps
    clock.tick(60)
    frame_counter +=1
    if launching and ball: #If the bird is being launched and there is a ball:

        #We set the image's position to be glued to the ball's position
        bird_pos.x = ball.body.position[0]
        bird_pos.y = ball.body.position[1]
        if frame_counter%3==0 and create_white_dot:
            l_white_dot.append((screen, "black", (bird_pos.x, bird_pos.y), 5))
    
    last_key = keys[pygame.K_p]
    #We draw evrything 
    draw(screen, space, draw_options, 
         bird, bird_pos, w,h, 
         ball, ball2 , ball3, 
         font, score, 
         background_image, cata, d_pig, pig, red, chuck, bomb, terence_for_show, terence, blues, matilda, king_pig, hammer, 
         building, placing, building_weight)

#We save the score in a text file
file = open("../LevelSave.txt","a")
file.write("Score:AngryBirds:"+str(score)+"\n")

file.close()

#We quit the game
pygame.quit()