# Projet_transverse
https://github.com/Marc35/Projet_transverse
Github du Projet transverse du semestre 2 en première année d'Efrei PARIS

Collaborateurs  : 
- FONTAINE Paul
-	PRAK Billy
-	BUCLON Mathis
-	DURIAUD Thomas

# Déscription rapide du projet
Dans ce jeu, vous trouverez 4 jeux réunis en un seul jeu toujours avec des trajectoires mais des gameplay totalement différents.

`pip install pymunk`

`pip install opencv-python`

# Manuels d'utilisation
- ## Bumped
  - ### Desciption
    Un jeu de type énigme où le but est de placer différents bumpers au bon endroit afin d'atteindre le drapeau à la fin d'un niveau.
  - ### Blocs
    - Bloc de bois : un simple bloc qui bloque la balle
    - Pics ou boule de pics : détruit la balle, le joueur doit relancer la balle
    - Portail antigravité : annule la gravité
    - Portail bleu / oranges : téléporte la balle du portail bleu vers le portail orange
  - ### Bumpers
    - Normal : fait simplement rebondir la balle
    - Speed : augmente la vitesse de la balle qui rebondira plus haut et plus loin
    - Inverse : inverse la gravité
  - ### Construction
    - Cliquez sur un objet et sur un endroit de la map pour le placer
    - Cliquez sur le curseur en haut à droite puis l'objet pour le sélectioner
    - Si vous êtes en édition de niveau :
      - Cliquez sur l'icône d'enregistrement pour enregistrer votre niveau
      - Cliquez sur la poubelle pour supprimer un niveau enregistré
      - Cliquez sur les plus ou les moins d'un type de bumpeur pour ajuster son nombre utilisable par le joueur
  - ### Keybinds :
     - F : déplacer un objet séléctionné
     - R : tourner un objet séléctionné
     - LEFT_ARROW : tourner de 45 degrés un objet séléctionné
     - ESPACE : lancer ou annuler le lancer de la balle
     - B : accéder au mode de placement des bumpers
     - SHIFT + A : accéder au mode éditeur de niveau
     - ESC : quitter le jeu et retourner au menu
