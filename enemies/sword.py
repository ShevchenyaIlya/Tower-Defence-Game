from enemies import enemy
from game.image_collection import ImageCollection


imgs = ImageCollection("enemies/", 20, 0, 100, 8, "_enemies_1_run_0")
imgs.download_images()

attack_imgs = ImageCollection("enemies/", 20, 0, 100, 8, "_enemies_1_attack_0")
attack_imgs.download_images()

die_imgs = ImageCollection("enemies/", 20, 0, 100, 8, "_enemies_1_die_0")
die_imgs.download_images()


class Sword(enemy.Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "sword"
        self.money = 50
        self.max_health = 100
        self.damage = 5
        self.armor = 2
        self.magick_resist = 2
        self.health = self.max_health
        self.active_imgs = imgs.images[:]
        self.attack_imgs = attack_imgs.images[:]
        self.die_imgs = die_imgs.images[:]
