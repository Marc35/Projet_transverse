import socket
import asyncore
import random
import pickle
import time
import math
import pygame

BUFFERSIZE = 512

outgoing = []
remove = []



def update_scoreboard(data):
    try:

        arr = pickle.load(data)
        if len(arr) < 3:
            print("Received data does not contain enough elements")
            return
        name = arr[1]

        name_is = False
        with open("players_scores.txt", "a+", encoding="utf-8") as fplayers:
            players_scores = fplayers.readlines()
            for players in players_scores:
                if name in players:
                    name_is = True

            if(arr[0] == "co" and name_is == False):
                fplayers.write("\n", name,":0")

            if(arr[0] == "point"):
                for players in players_scores:
                    if name in players:
                        players[len(name)+1:-1] = int(players[len(name)+1:-1]) +  int(arr[2])
        with open("players_scores.txt", "w", encoding="utf-8") as fplayers:
            for players in players_scores:
                fplayers.write(str(players))
                #modifier ligne pour ajouter les points en arr[0]


        if(arr == "update"):
            print("Update du scoreboard au joueur")
        

        for i in outgoing:
            try:
                i.send(pickle.dumps(players_scores))
            except Exception as e:
                print(f"Error sending update data: {e}")
                remove.append(i)

        for r in remove:
            outgoing.remove(r)
    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



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
        

        #conn.send(pickle.dumps(['id update', playerid]))
        SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
    def handle_read(self):
        recievedData = self.recv(BUFFERSIZE)
        if recievedData:
            update_scoreboard(recievedData)
        else: self.close()

MainServer(4322)
asyncore.loop()