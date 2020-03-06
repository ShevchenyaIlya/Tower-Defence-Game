import pygame
import os
from enemies import enemy
from towers.image_collection import ImageCollection


imgs = ImageCollection("enemies/", 20, 0, 100, 7, "_enemies_1_run_0")
imgs.download_images()


class Goblin(enemy.Enemy):
    def __init__(self):
        super().__init__()
        self.name = "sword"
        self.money = 35
        self.max_health = 25
        self.health = self.max_health
        self.imgs = imgs.images[:]
