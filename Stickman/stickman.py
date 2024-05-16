# Import
import pygame
import math
import pymunk
import pymunk.pygame_util
import random
from stickman_func import *

# _____pygame setup_____
pygame.init()
screen = pygame.display.set_mode((1600, 1000))
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

building = False
small_g = 9.81
dt = 0
font = pygame.font.Font('freesansbold.ttf', 32)
paused = False
capacity = False
mouse_B4 = False
placing = False
p_pressed = 0
r_pressed = 0
weight = 10
frame_counter = 0
gravity_multiplier = 100

chad = pygame.image.load('Gigachad.png').convert_alpha()
chad = pygame.transform.scale_by(chad, 0.15)

background_image = pygame.image.load("Shrek.jpg").convert()
background_image = pygame.transform.scale(background_image, (1600, 1000)) 
#________________________________________________________________________


space = pymunk.Space() #Generate the pymunk space
space.gravity = (0, 0) #Sets its gravity to 0,0 so we calculate it manually
draw_options = pymunk.pygame_util.DrawOptions(screen) #Give the pygame screen to pymunk

#Create the limit of the map
map_limit(space)

#Create a pig and add it to a list inside a dictionary
player = DummyV1(space, (1050,350))
player.addToSpace()
while running: #We loop while the game is running


    keys = pygame.key.get_pressed()#We get the current status of all keybord key

    for event in pygame.event.get():#We check the pygame event
        if event.type == pygame.QUIT: #If the user click the X
            running = False #We stop the loop
    
    #We apply the gravity to everything
    

    draw(screen, space, draw_options, background_image)
    #pygame.draw.rect(screen, "black", pygame.Rect(bird_pos.x, bird_pos.y, round((1-explosion_timer)*3200), round((1-explosion_timer)*3200)))
    
    #We check if prop should be destroyed
    event = mouse_event(mouse_B4) #get mouse event (check if mouse just got pressed/unpressed)

    #l_text = show_score_on_screens(l_text, dt, font, screen) # We show the text needed on screen

    for body in player.list_body:
        #body.angular_velocity = 0
        if body.angle > 0.3:
            body.angle -= 0.1
        elif body.angle < -0.3:
            body.angle += 0.1
    player.head_body.velocity += (0, -200)
    if keys[pygame.K_p]:
        if p_pressed == 0:
            p_pressed = 1
        else:
            p_pressed = -1
    if keys[pygame.K_r]:
        if r_pressed == 0:
            r_pressed = 1
        else:
            r_pressed = -1
    else:
        r_pressed = 0
    if p_pressed == 1:
        paused = not paused
        print(paused)
    if keys[pygame.K_z]:
        for body in player.list_body:
            body.velocity += (0, -500*dt*body.mass)

    if keys[pygame.K_s]:
         for body in player.list_body:
            body.velocity += (0, 500*dt*body.mass)
    if keys[pygame.K_q]:
         for body in player.list_body:
            body.velocity += (-500*dt*body.mass, 0)
    if keys[pygame.K_d]:
         for body in player.list_body:
            body.velocity += (500*dt*body.mass, 0)
    
    if r_pressed == 1:
        for body in player.list_body:
            body.angle = 0
            body.angular_velocity = 0
            body.velocity = (0,0)


    blitRotate(screen, chad, (player.head_body.position.x, player.head_body.position.y), (chad.get_size()[0]/2, chad.get_size()[1]/2), -1*player.head_body.angle*180/math.pi)
    if paused:
        pass
    else:
        player.apply_gravity(dt)
    #We remember the status of the mouse for the next when we will use mouse_event()
    mouse_B4 = clicking()

    #Display the game on the screen
    pygame.display.flip()

    #limits FPS to 60
    #dt is delta time in seconds since last frame, used for framerate-independent physics.
    #In simpler terms, dt is the time between each frame
    dt = clock.tick(60) / 1000
    if dt > 1/30:
        dt = 1/30

    space.step(dt) #We advance the simulation by dt so it stays logical even in case of higher/lower fps
    clock.tick(60)
    frame_counter +=1
pygame.quit()