#__________Import des extensions__________
import random
import time
import sys
import base64


#__________Objectifs du projets__________
def cahier_des_charges():   
    print('''
    Modifier les lettres des phrases données
    Rendre le plus difficile possible de décoder sans ce programme
    Pour cela:
    Une clé aléatoire sera choisie au moment de coder chaque message,
    Ensuite, la clé est modifié de maniére alétoire
    Cette nouvelle clé est rentrée dans une fonction choisie aléatoirement   
    La valeur de sortie est la postion dans l'alphabet de la nouvelle lettre, 
    

    Évolution:

    V1.0: Programme originale
    
    V1.1: Ajout des majuscules, des chiffres et ce 47 autres caractères
        Amélioration:
            Nbr de caractères traduit:
                27 --> 112
    
    V1.2: Optimisation du programme:
        Amélioration:
            Taille maximale d'un texte à traduire:
                10 --> 1 023
    
    V1.3: Mise en place d'une boucle permettant de répéter le programme sans avoir à le stopper
        Amélioration:
            Boucle:
                False --> True
    
    V1.4: Ajout de nouvelles fonctions/modificateur de clé/clé
        Amélioration:
            Nbr de combinaisons possible de fonctions/modificateur de clé/clé:
                300 --> 1 000 000
    ''')
#__________Boucle principal__________
loop = 1 #Permet à la boucle de ce lancer sans utiliser True au cas où on voudrait le stopper
while loop == 1: #La boucle relance le script en continue
    clear = ("\n\n\n") #Saute 3 ligne
    print(clear)

    #__________Message d'acceuil__________
    print("Bonjour !\nBienvenue sur la version 1.4 de Enigma\n")
    print('''Il est préférable de coder et décoder des phrases sans:
    saut de ligne,

    \nCaractères acceptés:
    Toutes les lettres de l'alphabet en minuscule + majuscule,
    Les chiffres, 
    Certains caractères tel que:
    ! # $ % & ( ) * + , - . ' " / : ; > < = ? @ [ ] ^ _ { } ~ € é è ê à â ç ù ô û É È À Â Ç Ù Ô Â Û

        \nQue voulez-vous faire ?
        \n1. Décodez un message
        \n2. Encodez un message
        \n3. Quitter
        \n\n\n''')
    
    
    #__________Initialisation des variables__________
    menu_choice = int(input("Choix: ")) #Demande à l'utilisateur ce qu'il veut faire
    print(clear)
    code_key = random.randint(1, 9999) #Génére une clé aléatoire
    key_choice = random.randint(1, 20) #Genere aléatoirement un modificateur de clé
    fonction = random.randint(1, 20) #Génére aléatoirement une fonction affine
    
    #On initialise à 0 des variables qu'on tuilise plus tard
    uncoded = str("NULL")  
    lettre = 0
    key = 0
    final_message = [] 
    coded_solved_message = [] 
    final_text = str()

    # Modifie la clé inital en fonction du modificateur de clé généré
    real_key1 = code_key * 5 + 2
    real_key2 = code_key * 8 + 3
    real_key3 = code_key * 3 + 4
    real_key4 = code_key * 9 + 5
    real_key5 = code_key * 8 + 12
    real_key6 = code_key * 7 + 2
    real_key7 = code_key * 6 + 17
    real_key8 = code_key * 9 + 6
    real_key9 = code_key * 10 + 7
    real_key10 = code_key * 13 + 4
    real_key11 = code_key * 12 + 8
    real_key12 = code_key * 11 + 14
    real_key13 = code_key * 15 + 13
    real_key14 = code_key * 16 + 22
    real_key15 = code_key * 18 + 25
    real_key16 = code_key * 17 + 21
    real_key17 = code_key * 19 + 9
    real_key18 = code_key * 20 + 4
    real_key19 = code_key * 24 + 32
    real_key20 = code_key * 22 + 21
    useless = str("Cette variable est pas vraiment utile mais c'est surtout que ça sert à rien de l'initialiser mais je me fais chier donc j'écris de la merde au lieu de faire mes exos de physique... Putin mais pourquoi je fais ce script en plus XD Y'a grave moyen que qq est déjà fait pareil duc on dirait juste que je le copier mais le pire que c'est que j'ai pas meme pas copier un seul morceau de code alors que ça aurait été tellement plus vite xD, si qq (autre que moi-meme hein !) lis-ça et bah passes une bonen journée ! (PASSEZ une bonne journée si c'est un adulte qui regarde ça)")

    # Modifie la clé inital en fonction du modificateur de clé généré
    if key_choice == 1:
        key = real_key1
    elif key_choice == 2:
        key = real_key2
    elif key_choice == 3:
        key = real_key3
    elif key_choice == 4:
        key = real_key4
    elif key_choice == 5:
        key = real_key5
    elif key_choice == 6:
        key = real_key6
    elif key_choice == 7:
        key = real_key7
    elif key_choice == 8:
        key = real_key8
    elif key_choice == 9:
        key = real_key9
    elif key_choice == 10:
        key = real_key10
    elif key_choice == 11:
        key = real_key11
    elif key_choice == 12:
        key = real_key12
    elif key_choice == 13:
        key = real_key13
    elif key_choice == 14:
        key = real_key14
    elif key_choice == 15:
        key = real_key15
    elif key_choice == 16:
        key = real_key16
    elif key_choice == 17:
        key = real_key17
    elif key_choice == 18:
        key = real_key18
    elif key_choice == 19:
        key = real_key19
    elif key_choice == 20:
        key = real_key20

    #__________Définition des fonction__________
    def encoding(lettre, key): #Fonction utilisée pour encoder un message
        #On crée un liste avec tout les caractères que l'on souhaite utiliser
        LISTE_LETTRE = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]"," ","^","_","{","}","~","€","ƒ","†","‰","‡","Š","Œ","Ž","š","œ","ž","Ÿ","¢","£","¥","§","¨","µ","¿","À","Á","Â","Ã","Ä","Å","Æ","Ç","È","É","Ê","Ë","Ì","Í","Î","Ï","Ð","Ñ","Ò","Ó","Ô","Õ","Ö","Ø","Ù","Ú","Û","Ü","Ý","ß","à","á","â","ã","ä","å","æ","ç","è","é","ê","ë","ì","í","î","ï","ñ","ò","ó","ô","õ","ö","÷","ø","ù","ú","û","ü","ý","ÿ"]
        
        for i in range(len(LISTE_LETTRE)): #On répéte autant de fois qu'il y a de valeur dans la liste LISTE_LETTRE
            if lettre == LISTE_LETTRE[i]: #Si la lettre que l'on cherche à encoder est égal à la lettre en position i dans LISTE_LETTRE:
                lettre = (i+1) #La lettre prend comme valeur sa place dans l'alphabet
                break #Une fois qu'on à trouve pour la bonne valeur on sort du "for i in range"
        
        while key > len(LISTE_LETTRE): #Tant que la clé est trop grande
            key -= len(LISTE_LETTRE) #On la réduit
        lettre += key #On ajoute la clé à lettre (Qui correspont actuellement à son emplacement dans la liste)
        while lettre > len(LISTE_LETTRE): #Si le nouvel emplacement de lettre sort de la liste
            lettre -= len(LISTE_LETTRE) #On le reduit pour qu'il soit bien dans la liste
        lettre = LISTE_LETTRE[lettre-1] #On attribut à lettre la nouvelle valeur coresspondante dans la list LISTE_LETTRE
        return lettre
    def function(key, key_choice, fonction): #Fonction utilisée pour modifier une clé
        #La clé est modifié par la fonction choisie au hasard à l'initialisation des variables
        if fonction == 1:
            key = key * 2 + 3
        elif fonction == 2:
            key = key * 4 + 6
        elif fonction == 3:
            key = key * 5 + 2
        elif fonction == 4:
            key = key * 3 + 4
        elif fonction == 5:
            key = key * 4 + 10
        elif fonction == 6:
            key = key * 8 + 12
        elif fonction == 7:
            key = key * 7 + 17
        elif fonction == 8:
            key = key * 9 + 43
        elif fonction == 9:
            key = key * 12 + 34
        elif fonction == 10:
            key = key * 14 + 18
        elif fonction == 11:
            key = key * 11 + 73
        elif fonction == 12:
            key = key * 18 + 14
        elif fonction == 13:
            key = key * 27 + 95
        elif fonction == 14:
            key = key * 28 + 37
        elif fonction == 15:
            key = key * 21 + 24
        elif fonction == 16:
            key = key * 19 + 16
        elif fonction == 17:
            key = key * 8 + 36
        elif fonction == 18:
            key = key * 13 + 79
        elif fonction == 19:
            key = key * 22 + 83
        elif fonction == 20:
            key = key * 23 + 62
        return key #Renvoie la nouvel clé
    def decoding(lettre, real_coded_key): #Fonction utilisée pour décoder un message
        #Donne pour chaque caractères, sa place dans l'alphabet
        LISTE_LETTRE = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]"," ","^","_","{","}","~","€","ƒ","†","‰","‡","Š","Œ","Ž","š","œ","ž","Ÿ","¢","£","¥","§","¨","µ","¿","À","Á","Â","Ã","Ä","Å","Æ","Ç","È","É","Ê","Ë","Ì","Í","Î","Ï","Ð","Ñ","Ò","Ó","Ô","Õ","Ö","Ø","Ù","Ú","Û","Ü","Ý","ß","à","á","â","ã","ä","å","æ","ç","è","é","ê","ë","ì","í","î","ï","ñ","ò","ó","ô","õ","ö","÷","ø","ù","ú","û","ü","ý","ÿ"]
        for i in range(len(LISTE_LETTRE)):
            if lettre == LISTE_LETTRE[i]:
                lettre = (i+1)
                break
        while real_coded_key > len(LISTE_LETTRE):
            real_coded_key -= len(LISTE_LETTRE)
        lettre -= real_coded_key
        while lettre <= 0:
            lettre += len(LISTE_LETTRE)
        lettre = LISTE_LETTRE[lettre-1]
        return lettre
    def encode2(message: str, encoding: str = "utf-8") -> str:
        # Encode the message as a bytes object
        message_bytes = message.encode(encoding)
        
        # Encode the bytes object as a base64 string
        base64_string = base64.b64encode(message_bytes)
        
        # Return the base64 string as a string
        return base64_string.decode(encoding)
    def decode2(base64_string: str, encoding: str = "utf-8") -> str:
        # Decode the base64 string as a bytes object
        message_bytes = base64.b64decode(base64_string)
        
        # Decode the bytes object as a string using the specified encoding
        return message_bytes.decode(encoding)
#__________Code__________

    #__________Décodage__________
    if menu_choice == 1 :
        coded_message1 = str(input("\n\nMessage: ")) #Demande à l'utilisateur le message à décoder
        print(coded_message1)
        coded_message = decode2(coded_message1)
        print(coded_message)
        coded_fonction = coded_message[0]
        listeF = ["&","§","+","£","€","*","$","@","#","à","o",",","!","?",";","/",":",".","(",")"]
        for i in range(20):
            if coded_fonction == listeF[i]:
                coded_fonction = i+1

        
        
        coded_create_key = coded_message[1]
        listeKC = ["A","f","'","é","ç","w","%","ù","è","P","=","-","4","0","7","z","S",")","<","g"]
        for i in range(20):
            if coded_create_key == listeKC[i]:
                coded_create_key = i+1
        
        num2str = ["b", "§", "ù", "à", "H", "%", "!", "3", "#", "S"]
        Tcoded_key = (coded_message[2]+coded_message[3]+coded_message[4]+coded_message[5])
        coded_key = ""
        for j in range(4):
            for i in range(10):
                if Tcoded_key[j] == num2str[i]:
                    coded_key += str(i)
        coded_key = int(coded_key)
        for i in range(6):
            coded_message = coded_message[1:]
        # Modifie la clé initiale en fonction du modificateur donné
        if coded_create_key == 1:
            real_coded_key = coded_key * 5 + 2
        elif coded_create_key == 2:
            real_coded_key = coded_key * 8 + 3
        elif coded_create_key == 3:
            real_coded_key = coded_key * 3 + 4
        elif coded_create_key == 4:
            real_coded_key = coded_key * 9 + 5
        elif coded_create_key == 5:
            real_coded_key = coded_key * 8 + 12
        elif coded_create_key == 6:
            real_coded_key = coded_key * 7 + 2
        elif coded_create_key == 7:
            real_coded_key = coded_key * 6 + 17
        elif coded_create_key == 8:
            real_coded_key = coded_key * 9 + 6
        elif coded_create_key == 9:
            real_coded_key = coded_key * 10 + 7
        elif coded_create_key == 10:
            real_coded_key = coded_key * 13 + 4
        elif coded_create_key == 11:
            real_coded_key = coded_key * 12 + 8
        elif coded_create_key == 12:
            real_coded_key = coded_key * 11 + 14
        elif coded_create_key == 13:
            real_coded_key = coded_key * 15 + 13
        elif coded_create_key == 14:
            real_coded_key = coded_key * 16 + 22
        elif coded_create_key == 15:
            real_coded_key = coded_key * 18 + 25
        elif coded_create_key == 16:
            real_coded_key = coded_key * 17 + 21
        elif coded_create_key == 17:
            real_coded_key = coded_key * 19 + 9
        elif coded_create_key == 18:
            real_coded_key = coded_key * 20 + 4
        elif coded_create_key == 19:
            real_coded_key = coded_key * 24 + 32
        elif coded_create_key == 20:
            real_coded_key = coded_key * 22 + 21
        
        for i in range(len(coded_message)): #Cette boucle se répéte pour chaque lettre du message
            lettre = str(coded_message[i]) #Prends une lettre (La 1ere si c'est le 1er tour de la boucle etc ...)
            lettre = decoding(lettre, real_coded_key) #Passes la lettre dans la fonction decoding(lettre, real_coded_key)
            coded_solved_message.append(str(lettre)) #Rajoutes la lettre dans la liste qui contiendra le message décoder
            real_coded_key = function(real_coded_key, coded_create_key, coded_fonction) #Modifie la clé grace à la fonction function(real_coded_key, coded_create_key, coded_fonction) 
            while real_coded_key > 10000: # Réduit la taille de la clé si celle-ci est trop grande (OPTIMISATION)
                real_coded_key = real_coded_key - 10000
        final_text = ''.join(coded_solved_message) # Regroupe chaque charachtères de la liste en un str
        print("\nMessage décodé:") 
        print("'"+final_text+"'") #Envoie le message décodé entre guillemets
        useless = input("\n\n\nAppuyer sur entrée pour revenir au menu") #Renvoie au menu

    #__________Encodage__________
    elif menu_choice == 2 : #Si l'utilisateur choisis d'encoder un message
        uncoded = str(input("Message: ")) #Demande à l'utilisateur le message à coder

        listeF = ["&","§","+","£","€","*","$","@","#","à","o",",","!","?",";","/",":",".","(",")"]
        afonction = listeF[fonction-1] #Transforme la valeur de la fonction en un caractéres à rajouter dans le message

        listeKC = ["A","f","'","é","ç","w","%","ù","è","P","=","-","4","0","7","z","S",")","<","g"]
        akey_choice = listeKC[key_choice-1] #Transforme la valeur de la clé en un caractéres à rajouter dans le message
        

        if code_key <= 9:
            code_key = ("000"+str(code_key))
        elif code_key <= 99:
            code_key = ("00"+str(code_key))
        elif code_key <= 999:
            code_key = ("0"+str(code_key))
        else:
            code_key = str(code_key)
        
        acode_key = ""
        num2str = ["b", "§", "ù", "à", "H", "%", "!", "3", "#", "S"]
        for i in range(len(code_key)):
            acode_key += num2str[int(code_key[i])]
        print("\n\n")
        print("\n\n")
        
        ####

        ####
        for i in range(len(uncoded)): #Cette boucle se répéte pour chaque lettre du message
            lettre = str(uncoded[i]) #Prends une lettre (La 1ere si c'est le 1er tour de la boucle etc ...)
            lettre = encoding(lettre, key) #Passes la lettre dans la fonction encoding(lettre, key)
            final_message.append(lettre) #Rajoutes la lettre dans la liste qui contiendra le message coder
            key = function(key, key_choice, fonction) #Modifie la clé grace à la fonction function(real_coded_key, coded_create_key, coded_fonction)
            while key > 10000: # Réduit la taille de la clé si celle-ci est trop grande (OPTIMISATION)
                key = key - 10000
        full_text = ''.join(final_message) # Regroupe chaque charachtères de la liste en un str
        full_message = afonction+akey_choice+acode_key+full_text
        #Fin de l'encodage 1
        #Encodage 2
        final_text = encode2(full_message)
        print("Message encodé:")
        print("'"+final_text+"'") #Envoie le message codé entre guillemets
        useless = input("\n\n\nAppuyer sur entrée pour revenir au menu") #Renvoie au menu
    
    #__________Quitter__________
    elif menu_choice == 3 :
        sys.exit()