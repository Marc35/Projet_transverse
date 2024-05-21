from Bumper_objectBuild import ObjectBuild

class Bumper(ObjectBuild):

    def __init__(self, image, pos, id, force_bounce, type, pos_plus, pos_moins, cpt=0):
        super().__init__(image, pos, id, force_bounce)
        #Pour le type de bumper
        self.type = type
        #Pour les compteurs par bumper
        if pos_plus != None and pos_moins != None:
            self.plus = ObjectBuild("FinalAssets/Build/Bumpers/plus.png", pos_plus, "plus")
            self.moins = ObjectBuild("FinalAssets/Build/Bumpers/moins.png", pos_moins, "moins")
        self.cpt = cpt

