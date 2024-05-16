import pygame
import math
import random as r
import sys

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 720))
screen_w, screen_h = (screen.get_width(), screen.get_height())

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
AQUA = 	(0,255,255)
MAGENTA = 	(255,0,255)

GRAVITY = (9.8)/4000

keys_B4 = {"z":0, "q":0, "s":0, "d":0, "space":0}

clock = pygame.time.Clock()
pygame.display.set_caption("Spider Dash")

font = pygame.font.Font('freesansbold.ttf', 32)
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
    [200,600, 200, 40],
]

all_portal = [
    [800,200,45, BLUE, "a\n"],#"a\n"
    [600,400,50, YELLOW, "b\n"],#"b\n"
    [400,600,50, AQUA, "c\n"],#"c\n"
    [1200,300,50, MAGENTA, "d\n"]#"d\n"
]

l_portal = []

file1 = open("LevelSave.txt","r")
lines = file1.readlines()
file1.close()
for portal in all_portal:
    if "a\n" not in lines:
        l_portal.append(all_portal[0])
    if "b\n" not in lines:
        l_portal.append(all_portal[1])
    if "c\n" not in lines:
        l_portal.append(all_portal[2])
    if "d\n" not in lines:
        l_portal.append(all_portal[3])

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

while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for prop in l_prop:
        pygame.draw.rect(screen, BLACK, (prop[0], prop[1], prop[2], prop[3]))
    for portal in l_portal:
        pygame.draw.circle(screen, portal[3], (portal[0], portal[1]), portal[2], 5)
        
    speed = 0.8
     
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
    elif not keys[pygame.K_z] and keys_B4["z"]:
        speed_y += speed
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
print(la_lettre)
file = open("LevelSave.txt", "a")
file.write(la_lettre)
file.close()
print("QUITTING MENU")
# Quit Pygame
#pygame.quit()

