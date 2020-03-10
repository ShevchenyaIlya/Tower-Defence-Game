import pygame
import os
from enemies import enemy
from towers.image_collection import ImageCollection


imgs = ImageCollection("enemies/", 20, 0, 64, 2, "_enemies_1_run_0")
imgs.download_images()

attack_imgs = ImageCollection("enemies/", 20, 0, 64, 2, "_enemies_1_attack_0")
attack_imgs.download_images()

die_imgs = ImageCollection("enemies/", 20, 0, 64, 2, "_enemies_1_die_0")
die_imgs.download_images()


class Wizard(enemy.Enemy):
    def __init__(self):
        super().__init__()
        self.name = "wizard"
        self.money = 3
        self.max_health = 3
        self.health = self.max_health
        self.imgs = imgs.images[:]
        self.attack_imgs = attack_imgs.images[:]
        self.die_imgs = die_imgs.images[:]



