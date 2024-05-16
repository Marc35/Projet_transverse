import socket
import asyncore
import random
import pickle
import time
import math
import pygame

BUFFERSIZE = 512

outgoing = []

screen_w, screen_h = 1600,720
l_prop = [[-100, screen_h-40, screen_w+200, 100], [-121, -100, 100, screen_h+150], [screen_w+21, -100, 100, screen_h+150], [-100, -100, screen_w+200, 100],
          [243, 214, 349, 59], [478, 435, 382, 88], [1070, 314, 439, 75]]
l_enemy = []
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


class Minion:
    def __init__(self, ownerid):
        self.x = 50
        self.y = 50
        self.w = 50
        self.h = 50
        self.skin_num = 0
        self.hp = 500
        self.score = 0
        self.s_x = -1
        self.s_y = -1
        self.l_laser = []
        self.l_bullet = []
        self.ownerid = ownerid

#[x, y, w, h, vx, vy, gravity, is_on_ground, monster_type, speed, apply_colision]
class Enemy:
    def __init__(self, x, y, w, h, mob_type, speed):
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.w = w
        self.h = h
        self.mob_type = mob_type
        self.speed = speed
        self.on_ground = False
        self.g = 0
    def get_close_player(self, player_list):
        lowest_dist = 100000
        close_player = None
        for player in player_list:
            distance = math.sqrt( (self.x-player.x)**2 + (self.y-player.y)**2)
            if distance < lowest_dist:
                lowest_dist = distance
                close_player = player
        return close_player
    def move_to_player(self, player_list):
        player = self.get_close_player(player_list)
        if player.x > self.x:
            self.v_x = self.speed
        elif player.x < self.x:
            self.v_x = -1*self.speed
        
        if self.mob_type == 1 or self.mob_type == 2:
            if player.y > self.y:
                self.v_y = self.speed
            elif player.y < self.y:
                self.v_y = -1*self.speed
    def apply_velocity(self, l_prop):
        self.v_y += self.g
        for prop in l_prop:
            if rectRect(self.x, self.y, self.w, self.h, prop[0], prop[1], prop[2], prop[3]) and self.mob_type != 2:
                self.v_y = 0
                if self.mob_type != 1:
                    self.g = 0
                self.on_ground = True
                
        if self.on_ground:
            self.g = 9.81
        touch_x = False
        touch_y = False
        if self.mob_type != 2:
            for prop in l_prop:
                if rectRect(self.x+self.v_x, self.y, self.w, self.h, prop[0], prop[1], prop[2], prop[3]):
                    touch_x = True
                if rectRect(self.x, self.y+self.v_y, self.w, self.h, prop[0], prop[1], prop[2], prop[3]):
                    touch_y = True
                if rectRect(self.x+self.v_x, self.y+self.v_y, self.w, self.h, prop[0], prop[1], prop[2], prop[3]) and not (touch_x or touch_y):
                    touch_x = True
                    touch_y = True
        
        if not touch_x:
            self.x += self.v_x
        if not touch_y:
            self.y += self.v_y
        else:
            self.v_y, self.g = 0,0
        while self.y > screen_h-self.h-50:
            self.y-=0.5
        while self.y < 0:
            self.y+=0.5

        while self.x > screen_w-self.w:
            self.x -= 0.5
        while self.x < 0:
            self.x += 0.5 

    def die(self, l_player):
        dead = False
        l_to_remove_bullet = []
        for player in l_player:
            for bullet in player.l_bullet:
                rect = pygame.Rect(self.x,self.y,self.w,self.h)
                if rect.clipline((bullet[0],bullet[1]), (bullet[0]+bullet[2]*20,bullet[1]+bullet[3]*20)):
                    player.score+=1000
                    l_to_remove_bullet.append(bullet)
                    dead = True
                    break
            player.l_bullet = [bullet for bullet in player.l_bullet if bullet not in l_to_remove_bullet]
            if dead:
                return player
        return False

    def kill(self, l_player):
        for player in l_player:
            if rectRect(self.x, self.y, self.w, self.h, player.x, player.y, player.w, player.h):
                player.hp -= 10
                return player
        return False
minionmap = {}

def updateWorld(message):
    global l_enemy
    try:
        arr = pickle.loads(message)
        #print(str(arr))
        if len(arr) < 13:
            print("Received data does not contain enough elements")
            return

        playerid = arr[1]
        x, y, w, h, skin_num, hp, score, s_x, s_y, l_laser, l_bullet = arr[2:13]

        if playerid == 0:
            return

        if playerid not in minionmap:
            print(f"Player with ID {playerid} not found in minion map")
            return
        
        minionmap[playerid].x = x
        minionmap[playerid].y = y
        minionmap[playerid].w = w
        minionmap[playerid].h = h
        minionmap[playerid].skin_num = skin_num
        minionmap[playerid].hp = hp
        minionmap[playerid].score = score
        minionmap[playerid].s_x = s_x
        minionmap[playerid].s_y = s_y
        minionmap[playerid].l_laser = l_laser
        minionmap[playerid].l_bullet = l_bullet
        remove = []
        update = ['player locations']

        if len(l_enemy)==0:
            l_enemy.append(Enemy(random.randint(200,1400), screen_h-110, 50, 50, 0, random.randint(7,14)))
            l_enemy.append(Enemy(random.randint(200,1400), screen_h-110, 50, 50, 1, random.randint(3,6)))
            l_enemy.append(Enemy(random.randint(200,1400), screen_h-110, 50, 50, 2, random.randint(3,4)))
        
        l_to_remove_enemy = []
        killer_player = False
        killed_player = False
        for enemy in l_enemy:
            enemy.move_to_player(minionmap.values())
            enemy.apply_velocity(l_prop) 
            
            killer_player = enemy.die(minionmap.values())  
            if killer_player:
                print(killer_player.l_bullet)
                l_to_remove_enemy.append(enemy)
            
            killed_player = enemy.kill(minionmap.values())
            if killed_player:
                l_to_remove_enemy.append(enemy)

        l_enemy = [enemy for enemy in l_enemy if enemy not in l_to_remove_enemy]

        for key, value in minionmap.items():
            update.append([value.ownerid, value.x, value.y, value.w, value.h, value.skin_num, value.hp, value.score, value.s_x, value.s_y, value.l_laser, value.l_bullet])
        
        

        add_on_list = [-1, l_enemy]

        if killer_player:
            if playerid == killer_player.ownerid:
                add_on_list.append(killer_player.score)
                add_on_list.append(killer_player.l_bullet)
            else:
                add_on_list.append(False)
                add_on_list.append(False)

        else:
            add_on_list.append(False)
            add_on_list.append(False)

        if killed_player:
            if playerid == killed_player.ownerid:
                add_on_list.append(killed_player.hp)
            else:
                add_on_list.append(False)
        else:
            add_on_list.append(False)

        print(add_on_list)
        update.append(add_on_list) 

        for i in outgoing:
            try:
                i.send(pickle.dumps(update))
                print("Sent update data")
            except Exception as e:
                print(f"Error sending update data: {e}")
                remove.append(i)

        for r in remove:
            outgoing.remove(r)
    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")
    #except Exception as e:
    #    print(f"An error occurred: {e}")


class MainServer(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(10)
    def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection address:' + addr[0] + " " + str(addr[1]))
        outgoing.append(conn)
        playerid = random.randint(1000, 1000000000)
        playerminion = Minion(playerid)
        minionmap[playerid] = playerminion
        
        conn.send(pickle.dumps(['id update', playerid]))
        SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
    def handle_read(self):
        recievedData = self.recv(BUFFERSIZE)
        if recievedData:
            updateWorld(recievedData)
        else: self.close()

MainServer(4321)
asyncore.loop()