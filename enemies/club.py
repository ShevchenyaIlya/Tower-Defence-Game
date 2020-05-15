from enemies import enemy
from game.image_collection import ImageCollection


imgs = ImageCollection("enemies/", 20, 0, 64, 5, "_enemies_1_run_0")
imgs.download_images()

attack_imgs = ImageCollection("enemies/", 20, 0, 64, 5, "_enemies_1_attack_0")
attack_imgs.download_images()

die_imgs = ImageCollection("enemies/", 20, 0, 64, 5, "_enemies_1_die_0")
die_imgs.download_images()


class Club(enemy.Enemy):
    def __init__(self, path, game_map):
        super().__init__(path, game_map)
        self.name = "club"
        self.money = 5
        self.damage = 1
        self.armor = 3
        self.magick_resist = 2
        self.active_imgs = imgs.images[:]
        self.attack_imgs = attack_imgs.images[:]
        self.die_imgs = die_imgs.images[:]
        self.max_health = 5
        self.health = self.max_health
