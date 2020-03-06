import pygame
import os
from enemies import enemy
from towers.image_collection import ImageCollection

"""imgs = []

for x in range(20):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("../game_assets/enemies/3", "3_enemies_1_run_0"
                                                                      + add_str + ".png")), (64, 64)))"""

imgs = ImageCollection("enemies/", 20, 0, 64, 3, "_enemies_1_run_0")


class Troll(enemy.Enemy):
    def __init__(self):
        super().__init__()
        self.name = "troll"
        self.money = 3
        self.imgs = imgs.images[:]
        self.max_health = 3
        self.health = self.max_health



