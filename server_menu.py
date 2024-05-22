import socket
import asyncore
import random
import pickle
import time
import math
import pygame
import os

BUFFERSIZE = 512

outgoing = []
remove = []


def update_scoreboard(data):
    try:
        #Si moins de 2 données sont reçu, il en manque donc forcément
        arr = pickle.loads(data)
        if len(arr) < 2:
            print("Received data does not contain enough elements")
            return
        name = arr[1]

        name_is = False
        players_scores = []
        with open("players_scores.txt", "r", encoding="utf-8") as fplayers:
            #Vérification si le nom du joueur est déja enregistré
            players_scores = fplayers.readlines()
            for players in players_scores:
                if name in players:
                    name_is = True

        with open("players_scores.txt", "a", encoding="utf-8") as fplayers:
            #arr[0] = 'co' signie que le joueur se connect pour la première fois, et name_is que son nom n'est pas dans le doc : initialisation des points du joueur
            if(arr[0] == "co" and name_is == False):
                fplayers.write(name +":0\n")

            # Si arr[0] = 'point', alors le joueur revient d'un niveau, et il le serveur lui ajoute des point à son total en mémoire
            # Avec arr[1] = nom du joueur et arr[2] = nb de point à ajouter 
            if(arr[0] == "point"):

                for i, players in enumerate(players_scores):
                    if name in players:
                        print(players)
                        print("SCORE ====", arr[2])
                        players_scores[i] = arr[1] + ":" + str(arr[2]) + "\n"



                print(players_scores)
                with open("players_scores.txt", "w", encoding="utf-8") as fplayers:
                    
                    for players in players_scores:
                        fplayers.write(str(players))
               
        #Lit le fichier une dernière fois en global pour transmettre les informations au ScoreBoard des joueurs 
        with open("players_scores.txt", "r", encoding="utf-8") as fplayers:
            
            players_scores = fplayers.readlines()

        #Signifie en console que le joueur reçoit des updates de son ScoreBoard
        if(arr[0] == "update_scoreboard"):
            print("Update du scoreboard au joueur")

        #Calcul dans le players_scores des 5 meilleurs joueurs afin de ne pas transmettre toute la liste aux joueurs connectés


        best_players = []
        temp_short = {}
        same_score = {}
        scores_list = []
        for players in players_scores:
            temp_nb = 0
            for c in players[:-1]:
                temp_nb += 1
                if(c == ':'):
                    break
            if(players[temp_nb:-1] in scores_list):
                temp_short[players[temp_nb:-1]] += players[:temp_nb-1]
                same_score[players[temp_nb:-1]].append(temp_nb-1)

                
            else:
                temp_short[players[temp_nb:-1]] = players[:temp_nb-1]
                same_score[players[temp_nb:-1]] = [temp_nb-1]
                scores_list.append(players[temp_nb:-1])
            
        
        # Convertir les éléments en entiers
        scores_list = [int(score) for score in scores_list]
        # Trier la liste en ordre décroissant
        scores_list.sort(reverse=True)
        scores_list = [str(score) for score in scores_list]


        if(len(scores_list) < 5):
            nb_player = len(scores_list)
        else:
            nb_player = 5

        max = 0
        for i in range(nb_player):
            temp = 0
            count = 0
            same = len(same_score[scores_list[i]])
            while(same != 0 and max < 5):
                best_players.append(temp_short[scores_list[i]][temp:(same_score[scores_list[i]][count]+temp)] + " : " + scores_list[i])
                temp += same_score[scores_list[i]][count]
                count += 1
                max += 1
                same -= 1




        for i in outgoing:
            try:
                i.send(pickle.dumps(best_players))
            except EOFError:
                print("EOFError: Client closed the connection.")
            #En cas de problème, le joueur est retiré de la liste des joueurs online
            except Exception as e:
                print(f"Error sending update data: {e}")
                remove.append(i)

        for r in remove:
            outgoing.remove(r)
            remove.remove(r)

        for r in remove:
            if r not in outgoing:
                remove.remove(r)
    #Exeptions en cas de problème de décompressage des données 
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
        
        SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
    def handle_read(self):
            try:
                recievedData = self.recv(BUFFERSIZE)
                print("TEST PICKLE ==== ", pickle.loads(recievedData))
                if recievedData:
                    update_scoreboard(recievedData)
                else: 
                    self.close()

            #Exeption en cas de déconnection du joueur : fermeture du socket lié au joueur sur le serveur
            except EOFError:
                print("EOFError: Client closed the connection.")
                self.close()

MainServer(4322)
asyncore.loop()