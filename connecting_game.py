import pygame
import math
import random as r
import sys
import os
from pygame.locals import *
import pickle
import select
import socket

# Save the name of the player
file = open("LevelSave.txt","r")
l_lines = file.readlines()
file.close()
if len(l_lines) == 1:
    first_connection = True
else:
    first_connection = False

# First connection


BUFFERSIZE = 4096
update_data = 0
time = 0
scoreboard = []
la_lettre = ""


if first_connection:
    

    pygame.init()



    display = pygame.display.set_mode((1600, 720))
    x, y = display.get_size()
    
    font = pygame.font.SysFont("Verdana", 20)
    pygame.display.set_caption("Menu")
    text_value = ""
    text = font.render(text_value, True, (255, 255, 255))
    fullscreen = False
    run = True
    #ajouter l'image de fond
    background_image = pygame.image.load("paysage3.jpeg").convert()
    background_image = pygame.transform.scale(background_image, (x, y))
    display.blit(background_image, (0, 0))

    
    while run:
        mouse_pos = pygame.mouse.get_pos()
        display.blit(background_image, (0, 0))
        if(text_value == ""):
            
            display.blit(font.render("Veuillez choisir un nom", True, (255, 0, 0)), (700, 360))
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        win = pygame.display.set_mode((x, y))
                if event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]
                    text = font.render(text_value, True, (255, 255, 255))
                if event.key == pygame.K_RETURN and text_value != "":              
                    run = False
                    pygame.quit
                    sys.exit

            if event.type == pygame.TEXTINPUT:
                text_value += event.text
                text = font.render(text_value, True, (255, 255, 255))
        display.blit(text, (700, 360))
        pygame.display.update()
        

    serverAddr = '141.94.37.226'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverAddr, 4322))
    ge = ['co', str(text_value)]
    s.send(pickle.dumps(ge))
    print("Connected to the server")
    print(text_value)
    # Save the name of the player
    file1 = open("LevelSave.txt","a")
    file1.write(text_value + "\n")
    file1.close()












# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 720))
screen_w, screen_h = (screen.get_width(), screen.get_height())
screen = pygame.display.set_mode((screen_w, screen_h))
background_image = pygame.image.load("paysage2.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen_w, screen_h))

portal1 = pygame.image.load("portal1.png").convert_alpha()
portal1 = pygame.transform.scale(portal1, (100, 100))
portal2 = pygame.image.load("portal2.png").convert_alpha()
portal2 = pygame.transform.scale(portal2, (100, 100))
portal3 = pygame.image.load("portal3.png").convert_alpha()
portal3 = pygame.transform.scale(portal3, (100, 100))
portal4 = pygame.image.load("portal4.png").convert_alpha()
portal4 = pygame.transform.scale(portal4, (100, 100))
portal5 = pygame.image.load("portal5.png").convert_alpha()
portal5 = pygame.transform.scale(portal5, (100, 100))

dirt = pygame.image.load("dirt.png").convert_alpha()
l_dirt = []

background_image = pygame.transform.scale(background_image, (screen_w, screen_h))   

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
AQUA = 	(0,255,255)
MAGENTA = 	(255,0,255)
GREEN = (0,255,0)

GRAVITY = (900.8)/400

score = 0

keys_B4 = {"z":0, "q":0, "s":0, "d":0, "space":0}

clock = pygame.time.Clock()
pygame.display.set_caption("Spider Dash")

font2 = pygame.font.Font('freesansbold.ttf', 32)
cube_x, cube_y = 300,300
speed_x, speed_y = 0,0
SIZE = 50

l_prop = [
    [-100,-100,1800,100],
    [-100,720,1800,100],
    [-100,-100,100,920],
    [1600,-100,100,920],

    [700,250, 200, 30],
    [180,200, 400, 50],
    [800,600, 300, 40],
    [700,370, 400, 30],
    [1200,480, 200, 40],
    [200,600, 200, 40]
]

for prop in l_prop:
    l_dirt.append(pygame.transform.scale(dirt, (prop[2], prop[3])))


all_portal = [
    [800,200,45, portal1, "a\n"],#"a\n"
    [380,150,50, portal2, "b\n"],#"b\n"
    [300,560,50, portal3, "c\n"],#"c\n"
    [1300,430,50, portal4, "d\n"],#"d\n"
    [1000,550,50, portal5, "e\n"]   
]

l_portal = []

file1 = open("LevelSave.txt","r")
lines = file1.readlines()
file1.close()
l_letter = []
for line in lines:
    l_letter.append(line[0])
print(l_letter)
if "a" not in l_letter:
    l_portal.append(all_portal[0])
if "b" not in l_letter:
    l_portal.append(all_portal[1])
if "c" not in l_letter:
    l_portal.append(all_portal[2])
if "d" not in l_letter:
    l_portal.append(all_portal[3])
    
l_portal.append(all_portal[4]) #On ajoute le dernier portail dans tous les cas cvar c'est le jeu en ligne.

for line in lines:
    print(line[:5])
    if line[:5] == "Score":
        score += int(line.split(":")[2])
        print("SCORE : ", score)

try:
    serverAddr = '141.94.37.226'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverAddr, 4322))
    ge = ["point", str(text_value), str(score)]
    s.send(pickle.dumps(ge))
    print("Value sent to the server")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Could not connect to the server")
# Main game loop
running = True

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

def receive_complete_data(socket, buffersize):
    received_data = b''
    while True:
        chunk = socket.recv(buffersize)
        if not chunk:
            break  # Connection closed, or no more data
        received_data += chunk
        if len(chunk) < buffersize:
            break  # Received less than expected, assume end of data
    return received_data

while running:


    # Client - Server connection 
    if update_data%10 == 0:
        try:
            ins, outs, ex = select.select([s], [], [], 0)
            for inm in ins: 
                #DATA EXCHANGE
                #RECEIVING DATA
                received_data = receive_complete_data(inm, BUFFERSIZE)
                menuEvent = pickle.loads(received_data)
                scoreboard = []
                for user in menuEvent:
                    scoreboard.append(user)
            ge = ['update_scoreboard', 'testing']
            s.send(pickle.dumps(ge))
                
                        
        except pickle.UnpicklingError as e:
            print(f"Error unpickling data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    

    update_data += 1

    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    for (dirt,prop) in zip(l_dirt,l_prop):
        screen.blit(dirt, (prop[0], prop[1]))
        
    for portal in l_portal:
        screen.blit(portal[3], (portal[0]-portal[2], portal[1]-portal[2]))
        
    speed = 25.8
    text = font2.render("___SCOREBOARD___", True, (255,0,0))
    textRect = text.get_rect()
    textRect.center = (1200, 50)
    screen.blit(text, textRect)
    for i in range(len(scoreboard)):
        text = font2.render(str(scoreboard[i]), True, (219,144,46))
        textRect = text.get_rect()
        textRect.center = (1200, 50+(i+1)*40)
        screen.blit(text, textRect)


    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("SCORE : ", True,(255,223,0))
    textRect = text.get_rect()
    textRect.center = (150, 20)
    screen.blit(text, textRect)

    text = font.render(str(score), True,(255,223,0))
    textRect = text.get_rect()
    textRect.center = (150, 70)
    screen.blit(text, textRect)



     
    if keys[pygame.K_q] and not keys_B4["q"]:
        speed_x -= speed
    elif not keys[pygame.K_q]and keys_B4["q"]:
        speed_x += speed
    if keys[pygame.K_d] and not keys_B4["d"]:
        speed_x += speed
    elif not keys[pygame.K_d] and keys_B4["d"]:
        speed_x -= speed
    if keys[pygame.K_z] and not keys_B4["z"]:
        speed_y -= speed
    if keys[pygame.K_s] and not keys_B4["s"]:
        speed_y += speed
    elif not keys[pygame.K_s] and keys_B4["s"]:
        speed_y -=speed
    
    if keys[pygame.K_SPACE]:
        for portal in l_portal:
            if rectRect(cube_x, cube_y, SIZE, SIZE, portal[0]-portal[2], portal[1]-portal[2], portal[2]*2, portal[2]*2):
                la_lettre= portal[4]
                running = False
                

    
    speed_y += GRAVITY

    touch_x, touch_y = False, False
    for prop in l_prop:
        if rectRect(cube_x+speed_x, cube_y, SIZE, SIZE, prop[0], prop[1], prop[2], prop[3]):
            touch_x = True
        if rectRect(cube_x, cube_y+speed_y, SIZE, SIZE, prop[0], prop[1], prop[2], prop[3]):
            touch_y = True
        if rectRect(cube_x+speed_x, cube_y+speed_y, SIZE, SIZE, prop[0], prop[1], prop[2], prop[3]) and not touch_x and not touch_y:
           touch_x, touch_y = True, True
    
    
    if not touch_x:
        cube_x+=speed_x
    if not touch_y:
        cube_y+=speed_y
    else:
        speed_y = 0
    pygame.draw.rect(screen, BLACK, (cube_x, cube_y, SIZE, SIZE))
    pygame.display.flip()
    
    keys_B4 = {"z":keys[pygame.K_z], "q":keys[pygame.K_q], "s":keys[pygame.K_s], "d":keys[pygame.K_d], "space":keys[pygame.K_SPACE]}
    dt = clock.tick(60) / 1000
    if dt > 1/30:
        dt = 1/60
    time+=dt
    clock.tick(60)
print(la_lettre)
file = open("LevelSave.txt", "a")
file.write(la_lettre)
file.close()
print("QUITTING MENU")
# Quit Pygame
pygame.quit()
