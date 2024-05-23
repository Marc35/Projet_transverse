import pygame
import math
import random as r
import os
import sys
from pygame.locals import *
import pickle
import select
import socket
 

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 720), pygame.RESIZABLE)
screen_w, screen_h = (screen.get_width(), screen.get_height())

clock = pygame.time.Clock()
pygame.display.set_caption("Spider Dash")
running_spider_dash = True
in_menu_spider_dash = True
end_screen_spider_dash = True

font = pygame.font.Font('freesansbold.ttf', 32)

# float
time =0.0
dt = 0.0
gravity = 9.81
angular_velocity = 0.0
wave_number = 0
#score = 0
#hp = 500
#Bool
mouse_B4 = [False, False]
grapped = False

#[x,y, duration, color]
l_particles = []
l_player = []
l_grap =  []
l_bullet = []
bullet = []
l_laser = []
#[-100, 681, 1800, 100], [-40, -10, 10, 750], [1620, -10, 10, 750], [-10, -10, 1650, 10]
        # The first 4 are the wall
l_prop = [[-100, screen_h-40, screen_w+200, 100], [-121, -100, 100, screen_h+150], [screen_w+21, -100, 100, screen_h+150], [-100, -100, screen_w+200, 100],
          [243, 214, 349, 59], [478, 435, 382, 88], [1070, 314, 439, 75]]

l_enemy = []

keys_B4 = {"z":0, "q":0, "s":0, "d":0, "space":0}
keys_pressed = {"z":0, "q":0, "s":0, "d":0}

heart_image = pygame.image.load("heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (50,50))

background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen_w, screen_h+150))

brick = pygame.image.load("brick.png").convert_alpha()
l_brick = []

for prop in l_prop:
    l_brick.append(pygame.transform.scale(brick, (prop[2], prop[3])))

def remove_from_list(lA, lB):
    """
    We remove from lA all items in lB
    """
    return [item for item in lA if item not in lB]

def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def clicking_l():#Send True if the mouse is pressed
    return pygame.mouse.get_pressed()[0]

def clicking_r():
    return pygame.mouse.get_pressed()[2]

def mouse_event_r(mouse_B4): #Give info about the state of the mouse's buttons
    """
    Return 1 at THE exact frame the mouse button is pressed
    Return -1 at THE exact frame the mouse button is unpressed
    Return 0 otherwise
    """
    #________________Check when mouse button is clicked/realeased________________
    if mouse_B4 == False and clicking_r() == True: 
        return 1
    elif mouse_B4 == True and clicking_r() == False:
        return -1
    return 0

def mouse_event_l(mouse_B4): #Give info about the state of the mouse's buttons
    """
    Return 1 at THE exact frame the mouse button is pressed
    Return -1 at THE exact frame the mouse button is unpressed
    Return 0 otherwise
    """
    #________________Check when mouse button is clicked/realeased________________
    if mouse_B4 == False and clicking_l() == True: 
        return 1
    elif mouse_B4 == True and clicking_l() == False:
        return -1
    return 0

def scalar(v1, v2):#Return the scalar of 2 vector
    """
    Return the scalar of 2 vector
    """
    if len(v1) != len(v2):
        raise ValueError("2 vec différents lors d'un scalire est impossible")
    summ =0
    for i in range(len(v1)):
        summ+=v1[i]*v2[i]
    return summ

def norm(vector):#Return the norm of a vector
    
    summ = 0
    for val in vector:
        summ +=val*val
    return math.sqrt(summ)

def draw(screen, background_image, heart_image, l_player, l_enemy,l_prop, l_particles, l_skin, l_laser, screen_h, screen_w, l_brick):
    """
    Draw everything needed for the game
    """
    screen.blit(background_image, (0, 0))#Draw the background
    
    for prop in l_prop: #For each prop
        #We draw it on the screen in black
        for (brick,prop) in zip(l_brick,l_prop):
            screen.blit(brick, (prop[0], prop[1]))

    for particle in l_particles:
        pygame.draw.circle(screen, particle[3], (particle[0], particle[1]), 5)

    for enemy in l_enemy: #For each enemy
        x = enemy[0]
        y = enemy[1]
        w = enemy[2]
        h = enemy[3]
        rect = pygame.Rect(enemy[0]-5, enemy[1]-5, enemy[2]+10, enemy[3]+10)
        pygame.draw.rect(screen, "white", rect)
        #We draw it depending on it's type so we give each one a different color
        rect = pygame.Rect(x, y, w, h)
        if enemy[8] == 0:
            pygame.draw.rect(screen, "red", rect)
        elif enemy[8] == 1:
            pygame.draw.rect(screen, "gold", rect)
        elif enemy[8] == 2:
            pygame.draw.rect(screen, "gray", rect)
    
    text = font.render("Score : "+str(l_player[0][14]), True,(255,255,255))
    textRect = text.get_rect()
    textRect.center = (100, screen_h-100)
    screen.blit(text, textRect)

    text = font.render("Vague : "+str(wave_number), True,(0,0,0))
    textRect = text.get_rect()
    textRect.center = (100, screen_h-200)
    screen.blit(text, textRect)
    
    for player in l_player: #We then draw the player
        x = player[0]
        y = player[1]
        w = player[2]
        h = player[3]
        rect = pygame.Rect(x-5, y-5, w+10, h+10)
        pygame.draw.rect(screen, "black", rect)
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, "white", rect)
        screen.blit(l_skin[player[11]], (x,y))
    for laser in l_laser:
        laser_x = laser[0]
        laser_y = laser[1]
        laser_axe = laser[2]
        laser_timer = laser[3]
        if (laser_axe == 0):
            if laser_timer >0:
                pygame.draw.line(screen, "orange", (laser_x, 0),(laser_x, screen_h), 5)
            else:
                pygame.draw.line(screen, "red", (laser_x, 0),(laser_x, screen_h), r.randint(10,30))
        elif (laser_axe == 1):
            if laser_timer >0:
                pygame.draw.line(screen, "orange", (0, laser_y),(screen_w, laser_y), 5)
            else:
                pygame.draw.line(screen, "red", (0, laser_y),(screen_w, laser_y), r.randint(10,30))
    text = font.render(str(l_player[0][13]), True,(255,0,0))
    textRect = text.get_rect()
    textRect.center = (100, 35)
    screen.blit(text, textRect)

    screen.blit(heart_image, (10,10))
def rectRect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h): #Say if 2 rectangles are touching each other
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

def apply_gravity(l_player):
    for i, player in enumerate(l_player): #For each player/enemy/anything in the list
        x = player[0]
        y = player[1]
        w = player[2]
        h = player[3]
        vx = player[4]
        vy = player[5]
        g = player[6]

        l_player[i][5] += g #We modify it's y velocity by g, the gravity, 9.81
    return l_player

def shoot(l_player):
    l_bullet = [] 
    for player in l_player: #We get the player info
        x = player[0]
        y = player[1]
        w = player[2]
        h = player[3]
        x_centered = x+w/2
        y_centered = y+h/2
        clicked_pos = pygame.mouse.get_pos() #We get clicked position
        shooting_d_x = x_centered - clicked_pos[0]
        shooting_d_y = y_centered - clicked_pos[1]

        #We prevent the case were it's equal to 0 because we will divide by it later
        if shooting_d_x == 0: 
            shooting_d_x = 0.1
        if shooting_d_y == 0:
            shooting_d_y = 0.1
        
        #We note by which value we should divid
        if abs(shooting_d_x) > abs(shooting_d_y):
            maxi = 0
        else:
            maxi = 1
        
        #We note the right x an y direction depending on how to mouse is compared to the player
        if shooting_d_x<0 and shooting_d_y<0:
            direction_x = 1
            direction_y = 1
        elif shooting_d_x>0 and shooting_d_y<0:
            direction_x = -1
            direction_y = 1
        elif shooting_d_x<0 and shooting_d_y>0:
            direction_x = 1
            direction_y = -1
        else:
            direction_x = -1
            direction_y = -1

        #Depending on which value we sould divid by, we do so, get the absoluta value so the sign dosen't bother us
        #And then we multiply by the direction to send the bullet in the right direction
        if maxi ==0:
            shooting_d_x, shooting_d_y = direction_x, abs(shooting_d_y/shooting_d_x)*direction_y
        else:
            shooting_d_x, shooting_d_y = abs(shooting_d_x/shooting_d_y)*direction_x, direction_y

        #We then add the bullet to the list
        l_bullet.append([x_centered,y_centered,shooting_d_x, shooting_d_y, 0])
    return l_bullet

def grappling(l_player):
    for player in l_player: #For each player
        #We get info
        x = player[0]
        y = player[1]
        w = player[2]
        h = player[3]
        x_centered = x+w/2
        y_centered = y+h/2
        clicked_pos = pygame.mouse.get_pos()
        shooting_d_x = x_centered - clicked_pos[0]
        shooting_d_y = y_centered - clicked_pos[1]

        #Really similar to the shoot() function
        #We shoot the graplin
        if shooting_d_x == 0:
            shooting_d_x = 0.1
        if shooting_d_y == 0:
            shooting_d_y = 0.1
        if shooting_d_x > shooting_d_y:
            maxi = 0
        else:
            maxi = 1
        if shooting_d_x<0 and shooting_d_y<0:
            if maxi ==0:
                shooting_d_x, shooting_d_y = 1, shooting_d_y/shooting_d_x
            else:
                shooting_d_x, shooting_d_y = shooting_d_x/shooting_d_y, 1
        else:
            if maxi ==0:
                shooting_d_x, shooting_d_y = -1, shooting_d_y/shooting_d_x*-1
            else:
                shooting_d_x, shooting_d_y = shooting_d_x/shooting_d_y*-1, -1
    return [x_centered,y_centered,shooting_d_x, shooting_d_y, 0] 

def apply_velocity(l_player, l_prop):
    for i, player in enumerate(l_player):
        x = player[0]
        y = player[1]
        w = player[2]
        h = player[3]
        vx = player[4]
        vy = player[5]
        collision = player[10]
        touch_x = False
        touch_y = False
        if collision:
            for prop in l_prop:
                if rectRect(x+vx, y, w, h, prop[0], prop[1], prop[2], prop[3]):
                    touch_x = True
                if rectRect(x, y+vy, w, h, prop[0], prop[1], prop[2], prop[3]):
                    touch_y = True
                if rectRect(x+vx, y+vy, w, h, prop[0], prop[1], prop[2], prop[3]) and not (touch_x or touch_y):
                    touch_x = True
                    touch_y = True
            if not touch_x:
                l_player[i][0] += vx
            if not touch_y:
                l_player[i][1] += vy
        else:
            l_player[i][0] += vx
            l_player[i][1] += vy
    return (l_player, touch_x, touch_y)

def enemy_mind(l_enemy, l_player):
    player  = l_player[0]
    for i, enemy in enumerate(l_enemy):
        x = enemy[0]
        y = enemy[1]
        w = enemy[2]
        h = enemy[3]
        mob_type = enemy[8]
        speed = l_enemy[i][9]
        if l_enemy[i][8] ==0:
            if player[0] > x:
                l_enemy[i][4] = speed
            elif player[0] < x:
                l_enemy[i][4] = -1*speed
        elif l_enemy[i][8] ==1 or l_enemy[i][8] ==2:
            if player[0] > x:
                l_enemy[i][4] = speed
            elif player[0] < x:
                l_enemy[i][4] = -1*speed
            if player[1] > y:
                l_enemy[i][5] = speed
            elif player[1] < y:
                l_enemy[i][5] = -1*speed
        elif mob_type ==0:
            pass
    return l_enemy

def calc_rotation_around_point(player, clicked_pos, angular_velocity):
    touch_x, touch_y = False, False
    angular_velocity *= math.pi/180
    distPlayerCenter_x = player[0] - clicked_pos[0]
    distPlayerCenter_y = player[1] - clicked_pos[1]
    x_new = distPlayerCenter_x * math.cos(angular_velocity) + distPlayerCenter_y * math.sin(angular_velocity) + clicked_pos[0]
    y_new = -1*distPlayerCenter_x * math.sin(angular_velocity) + distPlayerCenter_y * math.cos(angular_velocity) + clicked_pos[1]
    for prop in l_prop:
        if rectRect(x_new, y, w, h, prop[0], prop[1], prop[2], prop[3]):
           touch_x = True
        if rectRect(x, y_new, w, h, prop[0], prop[1], prop[2], prop[3]):
            touch_y = True
        if rectRect(x_new, y_new, w, h, prop[0], prop[1], prop[2], prop[3]) and not (touch_x or touch_y):
            touch_x = True
            touch_y = True
    if not touch_x:
        player[0] = x_new
    if not touch_y:
        player[1] = y_new
    return player, touch_x, touch_y
#laser = [x,y,axe(0=vertical,1=Horizontal), timer]
def time_laser(l_laser, dt):
    l_to_remove = []
    for i in range(len(l_laser)):
        l_laser[i][3]-=dt
        if l_laser[i][3] < -0.5:
            l_to_remove.append(l_laser[i])
    
    if len(l_to_remove) >0:
        l_laser = remove_from_list(l_laser, l_to_remove)
    return l_laser

def launch_laser(l_player, l_laser, screen_h, screen_w):
    x = l_player[0][0]
    y = l_player[0][1]
    w = l_player[0][2]
    h = l_player[0][3]
    rect = pygame.Rect(x,y,w,h)
    for laser in l_laser:
        laser_x = laser[0]
        laser_y = laser[1]
        laser_axe = laser[2]
        laser_timer = laser[3]
        if (laser_axe == 0 and laser_timer<0):
            if rect.clipline((laser_x, 0),(laser_x, screen_h)):
                l_player[0][13]-=1
        elif (laser_axe == 1 and laser_timer<0):
            if rect.clipline((0, laser_y),(screen_w, laser_y)):
                l_player[0][13]-=1
    return l_player


#[0, 1, 2, 3,  4,  5,       6,            7,        8,        9,             10,          11,       12, 13,    14]
#[x, y, w, h, vx, vy, gravity, is_on_ground, spider_x, spider_y, apply_colision, skin_number, can_dash, hp, score]
# x, y : Position of tha playerz
# w, h : Width and height of the player
# vx, vy : Velocity in the x and y axis
# gravity : The gravity constant associated with the player
# is_on_ground : 0=False, 1=True, says if the player is on the ground or not
l_player.append([200, 100, 50, 50, 0, 0, 9.81, 0, 0, 0, True, 0, True, 100, 0])
l_skin = list_of_files("./skin", ".png")
for i, skin in enumerate(l_skin):
    l_skin[i] = pygame.image.load("./skin/"+skin).convert_alpha()
    l_skin[i] = pygame.transform.scale(l_skin[i], (l_player[0][2],l_player[0][3]))
nb_skin = len(l_skin)
#[0, 1, 2, 3,  4,  5,       6,            7,            8,    9,              10]
#[x, y, w, h, vx, vy, gravity, is_on_ground, monster_type, speed, apply_colision]


#418;244;349;59 1290;352;439;75; 669;479;382;88
while in_menu_spider_dash:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            in_menu_spider_dash = False
            running_spider_dash = False
    
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            screen_w, screen_h = (screen.get_width(), screen.get_height())
            background_image = pygame.transform.scale(background_image, (screen_w, screen_h))
            l_prop[0], l_prop[1], l_prop[2], l_prop[3] = ([-100, screen_h-40, screen_w+200, 100], [-121, -100, 100, screen_h+150], [screen_w+21, -100, 100, screen_h+150], [-100, -100, screen_w+200, 100])
    
    if keys[pygame.K_RETURN]:
        in_menu_spider_dash = False
        running_spider_dash = True
    
    if keys[pygame.K_LEFT] and not keys_B4["left"]:
        l_player[0][11] = (l_player[0][11]-1)%nb_skin
    
    if keys[pygame.K_RIGHT] and not keys_B4["right"]:
        l_player[0][11] = (l_player[0][11]+1)%nb_skin
    
    rect = pygame.Rect(0, 0, screen_w, screen_h)
    pygame.draw.rect(screen, "gray", rect)
    
    text = font.render("Spider Dash", True,(255,0,0))
    textRect = text.get_rect()
    textRect.center = (800, 200)
    screen.blit(text, textRect)

    text = font.render("APPUYER SUR ENTREE POUR JOUER", True,(255,223,0))
    textRect = text.get_rect()
    textRect.center = (800, 700)
    screen.blit(text, textRect)

    text = font.render("<| Skin precedent                        Skin suivant |>", True,(0,0,0))
    textRect = text.get_rect()
    textRect.center = (800, 540)
    screen.blit(text, textRect)
    

    screen.blit(l_skin[l_player[0][11]], (800,525))

    pygame.display.flip()
    keys_B4 = {"z":keys[pygame.K_z], "q":keys[pygame.K_q], "s":keys[pygame.K_s], "d":keys[pygame.K_d], "space":keys[pygame.K_SPACE], "left":keys[pygame.K_LEFT], "right":keys[pygame.K_RIGHT]}

while running_spider_dash:
    keys = pygame.key.get_pressed()
    
    draw(screen, background_image, heart_image, l_player, l_enemy,l_prop, l_particles, l_skin, l_laser, screen_h, screen_w, l_brick)
    l_laser = time_laser(l_laser, dt)
    l_player = launch_laser(l_player, l_laser, screen_h, screen_w)
    #if r.uniform(0, 3/(time+0.01))*10<1:
    if time >3:
        time = 0
        l_laser.append([l_player[0][0]+l_player[0][2]/2,l_player[0][1]+l_player[0][3]/2,r.randint(0,1), 1])
    l_to_remove = []
    l_to_remove_bullet = []
    if len(l_enemy) == 0:
        for i in range(wave_number):
            enemy_type = r.choice([0,0,0,0,1,1,1,2,2])
            l_enemy.append([r.randint(200,1400), screen_h-110, r.randint(35,65), r.randint(35,65), 0, 0, 9.81, 0, enemy_type, r.randint(7-enemy_type*3,14-enemy_type*3), True if enemy_type!=2 else False])


            """l_enemy.append([r.randint(200,1400), screen_h-110, 50, 50, 0, 0, 9.81, 0, 0, r.randint(7,14), True])
            l_enemy.append([r.randint(200,1400),   screen_h-110, 50, 50, 0, 0, 9.81, 0, 1,  r.randint(3,6), True])
            l_enemy.append([r.randint(200,1400),   screen_h-110, 50, 50, 0, 0, 9.81, 0, 2,  r.randint(3,4), False])"""
        wave_number+=1
    for i, enemy in enumerate(l_enemy):
        x = enemy[0]
        y = enemy[1]
        w = enemy[2]
        h = enemy[3]
        x_centered = x+w/2
        y_centered = y+h/2
        if rectRect(x, y, w, h, 0, screen_h-40, screen_w, 120):

            l_enemy[i][5] = 0

            l_enemy[i][7] = 1
        else:            
            l_enemy[i][7] = 0
        for prop in l_prop:
            if rectRect(x, y, w, h, prop[0], prop[1], prop[2], prop[3]) and l_enemy[i][8] != 2:
                l_enemy[i][5] = 0
                l_enemy[i][7] = 1
        for bullet in l_bullet:
            rect = pygame.Rect(x,y,w,h)
            #if rect.clipline((b[0],b[1]), (b[0]+b[2]*20,b[1]+b[3]*20)):
            if rect.clipline((bullet[0],bullet[1]), (bullet[0]+bullet[2]*20,bullet[1]+bullet[3]*20)):
                l_to_remove.append(enemy)
                l_to_remove_bullet.append(bullet)
                l_player[0][14]+=1000
                for i in range(20):
                    l_particles.append([r.randint(-w,w)+x+w/2, r.randint(-h,h)+y+h/2, r.uniform(0.05, 0.4), r.choice(["red","orange","orange","yellow", "yellow", "yellow"])])
        if rectRect(x, y, w, h, l_player[0][0], l_player[0][1], l_player[0][2], l_player[0][3]) and enemy not in l_to_remove:
            l_to_remove.append(enemy)
            l_player[0][13]-=10
            for i in range(20):
                l_particles.append([r.randint(-w,w)+x+w/2, r.randint(-h,h)+y+h/2, r.uniform(0.05, 0.4), r.choice(["black","gray","gray","white", "white", "white"])])

    
    l_enemy = [enemy for enemy in l_enemy if enemy not in l_to_remove]
    l_bullet = [bullet for bullet in l_bullet if bullet not in l_to_remove_bullet]
    nb_popped_item = 0
    for i in range(len(l_particles)):
        l_particles[i-nb_popped_item][2] -= dt
        if l_particles[i-nb_popped_item][2]<0:
            l_particles.pop(i-nb_popped_item)
            nb_popped_item+=1

    for i, player in enumerate(l_player):
        x = player[0]
        y = player[1]
        w = player[2]
        h = player[3]
        x_centered = x+w/2
        y_centered = y+h/2

        """if rectRect(x, y, w, h, 0, 679, 1600, 120):

            l_player[i][5] = 0
            l_player[i][6] = 0

            l_player[i][7] = 1
        else:            
            l_player[i][7] = 0
        for prop in l_prop:
            if rectRect(x, y, w, h, prop[0], prop[1], prop[2], prop[3]):
                l_player[i][5] = 0
                l_player[i][6] = 0

                l_player[i][7] = 1
        if l_player[i][7] == 0:
            l_player[i][6] = 9.81"""
        
    
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_spider_dash = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            screen_w, screen_h = (screen.get_width(), screen.get_height())
            background_image = pygame.transform.scale(background_image, (screen_w, screen_h))
            l_prop[0], l_prop[1], l_prop[2], l_prop[3] = ([-100, screen_h-40, screen_w+200, 100], [-121, -100, 100, screen_h+150], [screen_w+21, -100, 100, screen_h+150], [-100, -100, screen_w+200, 100])

    event_l = mouse_event_l(mouse_B4[0])
    event_r = mouse_event_r(mouse_B4[1])
    
    if clicking_r() and grapped:
        
        pygame.draw.line(screen, "black", clicked_pos, (x_centered, y_centered))
        l_player[0][8] = x_centered - clicked_pos[0]
        l_player[0][9] = y_centered - clicked_pos[1]
        
        l_player[0][6] = 0

        if keys_pressed["z"]:
            keys_pressed["z"] = 0
            #l_player[0][5] += 600
            keys_B4["z"] = False
        if keys_pressed["s"]:
            keys_pressed["s"] = 0
            keys_B4["s"] = False
        if keys_pressed["d"]:
            keys_pressed["d"] = 0
            keys_B4["d"] = False
        if keys_pressed["q"]:
            keys_pressed["q"] = 0
            keys_B4["q"] = False
        if l_player[0][0] < clicked_pos[0]:
            angular_velocity +=1
        elif l_player[0][0] > clicked_pos[0]:
            angular_velocity -=1
        l_player[0], touch_x, touch_y = calc_rotation_around_point(l_player[0], clicked_pos, angular_velocity)
        if touch_x:
            angular_velocity /= 2
        if touch_y:
            angular_velocity /= 2
        
        
        grap_velocity = [l_player[0][8], l_player[0][9]]
        k = 1/norm(grap_velocity)
        multipler = 30
        l_player[0][4] = -1 * grap_velocity[0] * k * multipler
        l_player[0][5] = -1 * grap_velocity[1] * k * multipler
        """
        if l_player[0][7] == 0 or True: #to discuss bcs maybe but maybe not
            if l_player[0][0] < clicked_pos[0] and l_player[0][1] > clicked_pos[1]:
                l_player[0][4] += 2 
                l_player[0][5] -= 2

            elif l_player[0][0] > clicked_pos[0] and l_player[0][1] > clicked_pos[1]:
                l_player[0][4] -= 2 
                l_player[0][5] -= 2

            elif l_player[0][0] < clicked_pos[0] and l_player[0][1] < clicked_pos[1]:
                l_player[0][4] += 2 
                l_player[0][5] += 2

            elif l_player[0][0] > clicked_pos[0] and l_player[0][1] < clicked_pos[1]:
                l_player[0][4] -= 2 
                l_player[0][5] += 2"""
    else:
        clicked_pos = pygame.mouse.get_pos()
        l_player[0][8] = 0
        l_player[0][9] = 0
        l_player[0][6] = 9.81
    
    if event_r == 1:
        pos_when_clicked = (l_player[0][0]+l_player[0][2]/2,l_player[0][1]+l_player[0][3]/2)
        clicked_pos = pygame.mouse.get_pos()
        l_grap = grappling(l_player)
        grapped = False
        n = 0
        while not grapped:
            for prop in l_prop:
                rect = pygame.Rect(prop[0], prop[1], prop[2], prop[3])
                pygame.draw.line(screen, "black", (l_grap[0], l_grap[1]), (l_grap[0]+l_grap[2]*n, l_grap[1]+l_grap[3]*n), 3)
                if rect.clipline((l_grap[0], l_grap[1]), (l_grap[0]+l_grap[2]*n, l_grap[1]+l_grap[3]*n)):
                    grapped = True
                    clicked_pos= (l_grap[0]+l_grap[2]*n, l_grap[1]+l_grap[3]*n)
            if not grapped:
                n+=10
    elif event_r == -1:
        l_player[0][4] = 0
        l_player[0][5] = 0
        angular_velocity = 0
        if keys_pressed["d"] == 1:
            l_player[0][4] += 20
        if keys_pressed["q"] == 1:
            l_player[0][4] -= 20
        grapped = False
    
    bullet = []     
    
    if event_l == 1:
        bullet = shoot(l_player)
    
    for bull in bullet:

        l_bullet.append(bull)
    
    l_to_remove_bullet = []
    for i, b in enumerate(l_bullet):
        pygame.draw.line(screen, "yellow", (b[0],b[1]), (b[0]+b[2]*20,b[1]+b[3]*20), 10)
        
        for prop in l_prop:
            rect = pygame.Rect(prop[0], prop[1], prop[2], prop[3])
            if rect.clipline((b[0],b[1]), (b[0]+b[2]*20,b[1]+b[3]*20)):
                l_to_remove_bullet.append(b)
        b[4]+=1
        l_bullet[i][0] += b[4]*b[2]
        l_bullet[i][1] += b[4]*b[3]
    l_bullet = [bullet for bullet in l_bullet if bullet not in l_to_remove_bullet]   
    l_bullet_memo = l_bullet
    l_bullet = []
    for bull in l_bullet_memo:
        if bull[0] > screen_w+100 or bull[0] < -100 or bull[1] < -100 or bull[1] > screen_h+100:
            pass
        else:
            l_bullet.append(bull)
    
    if not keys_B4["z"] and keys[pygame.K_z] and not clicking_r() and keys_pressed["z"] == 0:
        l_player[0][5] -= 60
        keys_pressed["z"] = 1
        
    if not keys_B4["s"] and keys[pygame.K_s] and not clicking_r():
        l_player[0][5] += 20
        keys_pressed["s"] = 1
    elif keys_B4["s"] and not keys[pygame.K_s] and not clicking_r():
        keys_pressed["s"] = 0
        
    if not keys_B4["q"] and keys[pygame.K_q] and keys_pressed["q"] == 0 and not clicking_r():
        l_player[0][4] -= 20
        keys_pressed["q"] = 1
    elif keys_B4["q"] and not keys[pygame.K_q] and keys_pressed["q"] == 1 and not clicking_r():
        l_player[0][4] += 20
        keys_pressed["q"] = 0
        
    if not keys_B4["d"] and keys[pygame.K_d] and keys_pressed["d"] == 0 and not clicking_r():
        l_player[0][4] += 20
        keys_pressed["d"] = 1
    elif keys_B4["d"] and not keys[pygame.K_d] and keys_pressed["d"] == 1 and not clicking_r():
        l_player[0][4] -= 20
        keys_pressed["d"] = 0

    if not grapped and (keys_pressed["d"] == 0 and keys_pressed["q"] == 0) or (keys_pressed["d"] == 1 and keys_pressed["q"] == 1):
        l_player[0][4] = 0
    if not grapped and keys_pressed["d"] == 1 and keys_pressed["q"] == 0:
        l_player[0][4] = 20
    if not grapped and keys_pressed["d"] == 0 and keys_pressed["q"] == 1:
        l_player[0][4] = -20 
    
    #if not grapped and not keys_B4["space"] and keys[pygame.K_SPACE]:
    if not grapped and not keys_B4["space"] and keys[pygame.K_SPACE] and l_player[0][12]:
        dash_coords = [pygame.mouse.get_pos()[0] - x_centered, pygame.mouse.get_pos()[1] - y_centered]
        x = l_player[0][0]
        y = l_player[0][1]
        w = l_player[0][2]
        h = l_player[0][3]

        l_player[0][4] = 0
        l_player[0][5] = 0
        l_player[0][6] = 0
        colide = False

        k = 1/norm(dash_coords)

        dash_speed_x = dash_coords[0] * k
        dash_speed_y = dash_coords[1] * k
        multipler = 300
        for i in range(multipler):
            x = l_player[0][0]
            y = l_player[0][1]
            
            for prop in l_prop:
                if rectRect(x+dash_speed_x, y+dash_speed_y, w, h, prop[0], prop[1], prop[2], prop[3]):
                    colide = True
            
            if not colide:
                l_player[0][0] += dash_speed_x
                l_player[0][1] += dash_speed_y
                
                for i in range(1):
                    l_particles.append([r.randint(-w,w)+l_player[0][0]+w/2, r.randint(-h,h)+l_player[0][1]+h/2, r.uniform(0.05, 0.6), r.choice(["black","gray","gray","gray", "white", "white"])])
            else:
                break
        l_player[0][12] = False 
    l_player = apply_gravity(l_player)
    l_player, touch_x, touch_y = apply_velocity(l_player, l_prop)
    if touch_y:
        l_player[0][5] = 0
        l_player[0][6] = 0
        keys_pressed["z"], keys_pressed["s"] = 0,0
        l_player[0][12] = True

    if touch_x:
        l_player[0][4] = 0
        
        #keys_pressed["d"],keys_pressed["q"] = 0,0
        #WALL JUMP(removeable feature):
        l_player[0][12] = True
        keys_pressed["z"] = 0
    
    for i, player in enumerate(l_player):
        while l_player[i][1] > screen_h-h-40:
            l_player[i][1] -=0.5
        
        while l_player[i][1] < 0:
            l_player[i][1] +=0.5
        
        while l_player[i][0] < 0:
            l_player[i][0] +=0.5
        
        while l_player[i][0] > screen_w-w:
            l_player[i][0] -=0.5

    if len(l_enemy) >= 1:
        l_enemy = apply_gravity(l_enemy)
        l_enemy = enemy_mind(l_enemy, l_player)
        l_enemy, touch_x, touch_y = apply_velocity(l_enemy, l_prop)
    
    for i, enemy in enumerate(l_enemy):
        
        if touch_y and l_enemy[i][8] !=2:
            l_enemy[i][5] = 0

        while l_enemy[i][1] > screen_h-enemy[3]-50:
            l_enemy[i][1] -=0.5
        
        while l_enemy[i][1] < 0:
            l_enemy[i][1] +=0.5
        
        while l_enemy[i][0] < 0:
            l_enemy[i][0] +=0.5
        
        while l_enemy[i][0] > screen_w-enemy[2]:
            l_enemy[i][0] -=0.5
    if l_player[0][13] < 0:
        break
    mouse_B4 = [clicking_l(),clicking_r()]
    keys_B4 = {"z":keys[pygame.K_z], "q":keys[pygame.K_q], "s":keys[pygame.K_s], "d":keys[pygame.K_d], "space":keys[pygame.K_SPACE], "left":keys[pygame.K_LEFT], "right":keys[pygame.K_RIGHT]}
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    if dt > 1/30:
        dt = 1/60
    time+=dt
    clock.tick(60)

file = open("../LevelSave.txt","a")

file.write("Score:SpiderDash:"+str(l_player[0][14])+"\n")

file.close()

while end_screen_spider_dash:
    
    
    
    textRect = text.get_rect()
    textRect.center = (800, 200)
    screen.blit(text, textRect)

    text = font.render("APPUYER SUR ENTREE POUR QUITTER", True,(255,223,0))
    textRect = text.get_rect()
    textRect.center = (800, 700)
    screen.blit(text, textRect)

    text = font.render("YOU DIED", True,(255,0,0))
    textRect = text.get_rect()
    textRect.center = (800, 400)
    screen.blit(text, textRect)

    pygame.display.flip()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if keys[pygame.K_RETURN]:
        end_screen_spider_dash = False
        pygame.quit()
