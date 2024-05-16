import os
from math import *

file1 = open("LevelSave.txt","w")
file1.write("Levels:\n")
file1.close()


l_file = ['SpiderDash/spider_dash.py','AngryBirds/main2.py','./all.py', './']
running_connection = True
current_directory = os.getcwd()
while running_connection:

    # Chemin du fichier à exécuter
    os.chdir(current_directory)
    # Récupérer le répertoire de travail actuels

    #Run the main game that connects them all
    exec(open(os.path.basename("./connecting_game.py")).read())

    file = open("LevelSave.txt", "r")
    l_lines = file.readlines()
    file.close()
    print(l_lines)
    if l_lines[-1] == "a\n":
        file_to_run = l_file[0]
    elif l_lines[-1] == "b\n":
        file_to_run = l_file[1]
    elif l_lines[-1] == "c\n":
        file_to_run = l_file[2]
    elif l_lines[-1] == "d\n":
        file_to_run = l_file[3]
    else:
        print("BREAK BOI : ", l_lines[-1])
    # Changer le répertoire de travail
    os.chdir(os.path.dirname(file_to_run))

    # Exécuter le fichier
    exec(open(os.path.basename(file_to_run)).read())
    #Lorsque l'on termine le jeu:
    
    #Remet le répertoire de travail dans le dossier actuel
    

    #On passe au prochain jeu
print(running_connection)
exec(open(os.path.basename("connecting_game.py")).read())