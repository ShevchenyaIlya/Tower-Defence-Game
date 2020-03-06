import pygame
import os
from enemies import enemy
from towers.image_collection import ImageCollection


imgs = ImageCollection("enemies/", 20, 0, 64, 3, "_enemies_1_run_0")
imgs.download_images()


class Troll(enemy.Enemy):
    def __init__(self):
        super().__init__()
        self.name = "troll"
        self.money = 3
        self.imgs = imgs.images[:]
        self.max_health = 3
        self.health = self.max_health



