import pygame
from Bumper_objectBuild import ObjectBuild

class BluePortals(ObjectBuild):

    def __init__(self, image, pos, id, force_bounce):
        super().__init__(image, pos, id, force_bounce)
        self.red_portal = ObjectBuild("FinalAssets/Build/Modificateurs/Tp_portal/red_portal.png", (pygame.mouse.get_pos()[0] + 100, pygame.mouse.get_pos()[1]),"red_portal")