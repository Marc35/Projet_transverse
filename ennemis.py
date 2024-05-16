import pygame
import items
class Ennemis(items.Items):

    def __init__(self, pos):
        super().__init__(pos, "Assets/Images/Ennemis/pig.png")