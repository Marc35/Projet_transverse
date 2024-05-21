from Bumper_objectBuild import ObjectBuild
from Bumper_bumper import Bumper
from Bumper_portals import BluePortals
from math import *
import pygame



class Build:

    def __init__(self):
        #Attribut d'Etats
        self.is_placing = False
        self.is_mouving = False
        #Attributs d'outils
        self.save = ObjectBuild("FinalAssets/Build/Outils/save.png", (990, 2), "save")
        self.suppr = ObjectBuild("FinalAssets/Build/Outils/suppr.png", (925, 10), "suppr")
        self.finish = ObjectBuild("FinalAssets/Build/Outils/check.png", (1125, 5), "check")
        self.choice_mouving = ObjectBuild("FinalAssets/Build/Outils/choice.png", (1215, 5), "choice")
        self.next = ObjectBuild("FinalAssets/Build/Outils/next.png", (825, 5), "next")
        self.previous = ObjectBuild("FinalAssets/Build/Outils/previous.png", (720, 5), "previous")
        # Pour le block de fin
        self.fin = ObjectBuild("FinalAssets/Build/Fin.png", (642, 10), "fin")
        self.fin.reset_visuel(0.5)
        #Pour les choix de combien de bumpers
        self.bump_classique = Bumper("FinalAssets/Build/Bumpers/normal_bump.png", (1215, 120), "bumper", 1, "exemple", (1207, 83), (1247, 83))
        self.bump_classique.reset_visuel(0.75, 90)
        self.bump_speed = Bumper("FinalAssets/Build/Bumpers/speed_bump.png", (1215, 275), "bumper", 1, "exemple", (1207, 237), (1247, 237))
        self.bump_speed.reset_visuel(0.75, 90)
        self.bump_gravity = Bumper("FinalAssets/Build/Bumpers/gravity_bump.png", (1215, 437), "bumper", 1, "exemple", (1207, 402), (1247, 402))
        self.bump_gravity.reset_visuel(0.75, 90)
        #Attribut de choix de blocs
        self.choice_wall_wood = ObjectBuild("FinalAssets/Build/Blocs/WoodBloc.png", (105, 25), "wall_wood")
        self.choice_wall_wood.reset_visuel((95, 13))
        self.choice_tile = ObjectBuild("FinalAssets/Build/Blocs/Tile.png", (39, 25), "tile")
        self.choice_spikes = ObjectBuild("FinalAssets/Build/Danger/spike.png", (210, 5), "spike")
        self.choice_crystal = ObjectBuild("FinalAssets/Build/Danger/crystal.png", (250, 5), "crystal")
        self.choice_StopGravity_portal = ObjectBuild("FinalAssets/Build/Modificateurs/StopGravity_portal.png", (315, 5), "StopGravity_portal")
        self.choice_StopGravity_portal.reset_visuel(0.5)
        self.choice_blue_portal = ObjectBuild("FinalAssets/Build/Modificateurs/Tp_portal/blue_portal.png", (360, 5), "blue_portal")
        self.choice_blue_portal.reset_visuel(0.5)
        self.choice_red_portal = ObjectBuild("FinalAssets/Build/Modificateurs/Tp_portal/red_portal.png", (360, 40), "blue_portal")
        self.choice_red_portal.reset_visuel(0.5)
        self.red_portal_pos_to_build = []
        self.choose = None          #Objet choisi en str
        self.is_selected = None     #Objet choisi en instance d'objet
        # Pour les bumpers
        self.is_preselected = None
        #Attribut de level
        self.level_build = []   #Contient une seule map
        self.mapToBuild = -1
        #Liste de barre de choix
        self.outils = [self.choice_wall_wood, self.save, self.suppr, self.finish, self.choice_mouving, self.next, self.previous, self.bump_classique, self.bump_classique.plus, self.bump_classique.moins, self.bump_speed, self.bump_speed.moins, self.bump_speed.plus, self.bump_gravity, self.bump_gravity.plus, self.bump_gravity.moins, self.choice_spikes, self.choice_crystal, self.choice_StopGravity_portal, self.choice_blue_portal, self.choice_red_portal, self.choice_tile, self.fin]


    def reset_nb_bump(self, obj):
        obj.cpt = obj.plus.nb - obj.moins.nb
        if obj.cpt < 0:
            obj.plus.nb = 0
            obj.moins.nb = 0
            obj.cpt = 0

    def set_nb_bump(self, nb1=None, nb2=None, nb3=None):
        if nb1 is not None:
            self.bump_classique.cpt = nb1
            self.bump_classique.plus.nb = nb1
            self.bump_classique.moins.nb = 0
        if nb2 is not None:
            self.bump_speed.cpt = nb2
            self.bump_speed.plus.nb = nb2
            self.bump_speed.moins.nb = 0
        if nb3 is not None:
            self.bump_gravity.cpt = nb3
            self.bump_gravity.plus.nb = nb3
            self.bump_gravity.moins.nb = 0

    def choice(self, obj):
        """
        Permet à l'utilisateur de choisir qq chose dans la barre d'outils
        :param obj: L'objet sur lequel l'utilisateur a cliqué
        """
        match obj.id:
            # Met les présets en fonction de l'objet choisi
            case "suppr":
                if self.mapToBuild >= 0:
                    self.delete_map()
                else:
                    self.level_build = []
            case "save":
                if self.level_build != []:
                    self.saving()
            case "next":
                with open("maps.txt", "r") as file:
                    nb_maps = len(file.readlines())
                if self.mapToBuild < nb_maps-1:
                    self.mapToBuild += 1
                    self.building()
            case "previous":
                if self.mapToBuild >= -1:
                    self.mapToBuild -= 1
                    self.building()
            case "choice":
                self.choose = None
                self.is_mouving = True
                self.is_placing = False
            case "wall_wood":
                self.choose = self.choice_wall_wood.id
                self.is_placing = True
                self.is_mouving = False
            case "tile":
                self.choose = self.choice_tile.id
                self.is_placing = True
                self.is_mouving = False
            case "spike":
                self.choose = self.choice_spikes.id
                self.is_placing = True
                self.is_mouving = False
            case "crystal":
                self.choose = self.choice_crystal.id
                self.is_placing = True
                self.is_mouving = False
            case "fin":
                self.choose = self.fin.id
                self.is_placing = True
                self.is_mouving = False
            case "StopGravity_portal":
                self.choose = self.choice_StopGravity_portal.id
                self.is_placing = True
                self.is_mouving = False
            case "blue_portal":
                self.choose = self.choice_blue_portal.id
                self.is_placing = True
                self.is_mouving = False
            case "plus":
                obj.nb += 1
            case "moins":
                obj.nb += 1
            case "bumper":
                # Si c un bumper regarde quel type
                match obj.type:
                    case "exemple":
                        self.choose = None
                        self.is_placing = False
                        self.is_mouving = False
                    case "normal":
                        self.is_preselected = self.bump_classique
                        self.choose = "normal"
                        self.is_placing = True
                        self.is_mouving = False
                    case "speed":
                        self.is_preselected = self.bump_speed
                        self.choose = "speed"
                        self.is_placing = True
                        self.is_mouving = False
                    case "gravity":
                        self.is_preselected = self.bump_gravity
                        self.choose = "gravity"
                        self.is_placing = True
                        self.is_mouving = False

    def select(self, obj):
        """
        Permet de sauvegarder quel outils a été selectioné
        :param obj: L'objet sur lequel l'utilisateur a cliqué
        """
        self.is_selected = obj
        if obj.id == "bumper":
            match obj.type:
                case "normal":
                    self.is_preselected = self.bump_classique
                case "speed":
                    self.is_preselected = self.bump_speed
                case "gravity":
                    self.is_preselected = self.bump_gravity

    def delete(self):
        """
        Permet de supprimer un objet
        """
        if self.is_selected.id == "bumper":
            self.choose = self.is_selected.type
        self.level_build.remove(self.is_selected)
        self.is_selected = None

    def rotate(self, angle=None):
        """
        Permet de rotationer un objet
        :param angle: Si pas donné on calcule l'angle de rotation par rapport a la souris / Si donné on utilise l'angle de rotation donné
        """
        # Pour calculer l'angle
        if angle == None:
            self.is_selected.angle = atan2((self.is_selected.rect.y + self.is_selected.rect[3] // 2 - pygame.mouse.get_pos()[1]),
                      (pygame.mouse.get_pos()[0] - self.is_selected.rect.x - self.is_selected.rect[2] // 2)) * (180 / pi) - 100
        else:
            self.is_selected.angle += angle
        # L'angle renvoyé est entre -280 et 80, on la rapporte à 0 - 360
        self.is_selected.angle = (self.is_selected.angle+360)%360
        # Pour trouver les nouveaux points qui forment la plateforme après rotate
        m = (int(self.is_selected.sauv_pos_x + self.is_selected.sauv_height/2), int(self.is_selected.sauv_pos_y + self.is_selected.sauv_width / 2))
        point_centre2 = (m[0] - self.is_selected.sauv_height/2 * cos(self.is_selected.angle * (pi / 180)), m[1] + self.is_selected.sauv_height/2 * sin(self.is_selected.angle * (pi / 180)))
        point_centre1 = (m[0] + self.is_selected.sauv_height/2 * cos(self.is_selected.angle * (pi / 180)), m[1] - self.is_selected.sauv_height/2 * sin(self.is_selected.angle * (pi / 180)))
        self.is_selected.points[0] = [point_centre2[0] - self.is_selected.sauv_width/2 * sin(self.is_selected.angle * (pi/180)), point_centre2[1] - self.is_selected.sauv_width/2 * cos(self.is_selected.angle * (pi/180))]
        self.is_selected.points[1] = [point_centre2[0] + self.is_selected.sauv_width/2 * sin(self.is_selected.angle * (pi/180)), point_centre2[1] + self.is_selected.sauv_width/2 * cos(self.is_selected.angle * (pi/180))]
        self.is_selected.points[2] = [point_centre1[0] - self.is_selected.sauv_width/2 * sin(self.is_selected.angle * (pi/180)), point_centre1[1] - self.is_selected.sauv_width/2 * cos(self.is_selected.angle * (pi/180))]
        self.is_selected.points[3] = [point_centre1[0] + self.is_selected.sauv_width/2 * sin(self.is_selected.angle * (pi/180)), point_centre1[1] + self.is_selected.sauv_width/2 * cos(self.is_selected.angle * (pi/180))]
        # Pour rotate
        center = (self.is_selected.rect.x + self.is_selected.rect[2] // 2, self.is_selected.rect.y + self.is_selected.rect[3] // 2)
        self.is_selected.image = pygame.transform.rotate(self.is_selected.image_base, self.is_selected.angle)
        self.is_selected.rect = self.is_selected.image.get_rect(center=center)

    def place(self, pos, angle=None):
        """
        Permet de placer l'objet sélectionné par l'utilisateur
        :param pos: La position du futur objet
        :param angle: L'angle de rotation si l'objet que l'on veut placé a déja une rotation sinon si ce paramétre est a None on placera l'objet horizontalement
        """
        posToPlace = (pos[0] - pos[0] % (self.choice_spikes.rect[2] - 3), pos[1] - pos[1] % (self.choice_spikes.rect[3] - 3))
        match self.choose:
            case "wall_wood":
                nouv_item = ObjectBuild("FinalAssets/Build/Blocs/WoodBloc.png", posToPlace, "wall_wood", 0.2)
            case "tile":
                nouv_item = ObjectBuild("FinalAssets/Build/Blocs/Tile.png", posToPlace, "tile", 0.2)
            case "fin":
                nouv_item = ObjectBuild("FinalAssets/Build/Fin.png", posToPlace, "fin")
            case "spike":
                nouv_item = ObjectBuild("FinalAssets/Build/Danger/spike.png", posToPlace, "spike")
            case "crystal":
                nouv_item = ObjectBuild("FinalAssets/Build/Danger/crystal.png", posToPlace, "crystal")
            case "StopGravity_portal":
                nouv_item = ObjectBuild("FinalAssets/Build/Modificateurs/StopGravity_portal.png", posToPlace, "StopGravity_portal", -1)
            case "blue_portal":
                nouv_item = BluePortals("FinalAssets/Build/Modificateurs/Tp_portal/blue_portal.png", posToPlace, "blue_portal", -1)
                if self.red_portal_pos_to_build != []:
                    nouv_item.red_portal.rect.x = self.red_portal_pos_to_build[0]
                    nouv_item.red_portal.rect.y = self.red_portal_pos_to_build[1]
                    nouv_item.red_portal.sauv_pos_x = self.red_portal_pos_to_build[0]
                    nouv_item.red_portal.sauv_pos_y = self.red_portal_pos_to_build[1]
                self.level_build.append(nouv_item.red_portal)
            case "red_portal":
                self.red_portal_pos_to_build = pos

        if self.choose != "red_portal":
            if angle != None:
                nouv_item.angle = angle
                self.is_selected = nouv_item
                self.rotate(0)
            self.level_build.append(nouv_item)

    def mouv(self):
        """
        Permet de déplacé un objet déja posé et séléctionné par le joueur
        """
        self.is_selected.rect.x = pygame.mouse.get_pos()[0] - self.is_selected.rect[2]/2
        self.is_selected.rect.y = pygame.mouse.get_pos()[1] - self.is_selected.rect[3]/2
        self.is_selected.sauv_pos_x = pygame.mouse.get_pos()[0] - self.is_selected.sauv_height/2
        self.is_selected.sauv_pos_y = pygame.mouse.get_pos()[1] - self.is_selected.sauv_width/2

    def saving(self):
        """
        Permet de sauvegarder une map
        """
        with open("maps.txt", "a") as doc:
            doc.write(str(self.bump_classique.cpt) + "," + str(self.bump_speed.cpt) + "," + str(self.bump_gravity.cpt) + ";")
            for i in self.level_build:
                doc.write(i.id + "," + str(i.sauv_pos_x) + "," + str(i.sauv_pos_y) + "," + str(i.angle) + ";")
            doc.write("\n")

    def delete_map(self):
        """
        Permet de supprimer une map
        """
        self.level_build = []
        with open("maps.txt", "r") as doc:
            lignes = doc.readlines()
        with open("maps.txt", "w") as doc:
            doc.writelines(lignes[:self.mapToBuild])
            doc.writelines(lignes[self.mapToBuild+1:])
        self.mapToBuild = -1

    def building(self):
        """
        Permet de reconstruire une map sauvegardée
        """
        self.level_build = []
        self.set_nb_bump(0, 0, 0)
        if self.mapToBuild > -1:
            with open("maps.txt", "r") as doc:
                lignes = doc.readlines()
                objets = lignes[self.mapToBuild].split(";")[1:]
                objets.pop()
                for objet in objets:
                    infos_obj = objet.split(",")
                    self.choose = infos_obj[0]
                    self.place((float(infos_obj[1]), float(infos_obj[2])), float(infos_obj[3]))
                bumpers = lignes[self.mapToBuild].split(";")[:1]
                infos_bumpers = bumpers[0].split(",")
                self.set_nb_bump(int(infos_bumpers[0]), int(infos_bumpers[1]), int(infos_bumpers[2]))

