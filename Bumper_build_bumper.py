from Bumper_build import *

class Build_bumper(Build):

    def __init__(self):
        super().__init__()
        # Pour l'objet bumper
        self.bump_classique = Bumper("FinalAssets/Build/Bumpers/normal_bump.png", (0, 5), "bumper", 1, "normal", None, None)
        self.bump_speed = Bumper("FinalAssets/Build/Bumpers/speed_bump.png", (125, 5), "bumper", 1, "speed", None, None)
        self.bump_gravity = Bumper("FinalAssets/Build/Bumpers/gravity_bump.png", (260, 5), "bumper", 1, "gravity", None, None)
        #Pour les outils
        self.outils = [self.choice_mouving, self.bump_classique, self.bump_speed, self.bump_gravity, self.finish]
        #Pour la liste des bumpers
        self.level_build = []

    def place_bumper(self, pos):
        if self.is_preselected.cpt > 0:
            match self.choose:
                case "normal":
                    nouv_bumper = Bumper("FinalAssets/Build/Bumpers/normal_bump.png", pos, "bumper", 1, "normal", None, None)
                case "speed":
                    nouv_bumper = Bumper("FinalAssets/Build/Bumpers/speed_bump.png", pos, "bumper", 1, "speed", None, None)
                case "gravity":
                    nouv_bumper = Bumper("FinalAssets/Build/Bumpers/gravity_bump.png", pos, "bumper", 1, "gravity",None, None)
            self.level_build.append(nouv_bumper)

    def reset_bumper(self, nb):
        if self.is_preselected.cpt >= -nb:
            self.is_preselected.cpt += nb
