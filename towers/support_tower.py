import pygame
from towers.tower import Tower
import os
import math
from towers.image_collection import ImageCollection

"""range_imgs = []
for index in range(2):
    range_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("../game_assets/towers/support tower/1", "support_tower_1("
                                                     + str(index) + ").png")), (90, 90)))"""

range_imgs = ImageCollection("../game_assets/towers/support tower/1/", 3, 1, 90, 0, "support_tower_1_")
range_imgs.download_tower()


class RangeTower(Tower):
    """
    Add extra range to each surrounding tower
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 85
        self.effect = [0.2, 0.4]
        self.tower_imgs = range_imgs.images[:]
        self.width = self.height = 90
        self.name = "range"
        self.price = 1000

        # define menu and buttons
        # self.menu = Menu(self, self.x, self.y, menu_bg, [2000, "Max"])
        # self.menu.add_btn(upgrade_btn, "Upgrade")

    def get_upgrade_cost(self):
        return self.menu.get_item_cost()

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def support(self, towers):
        """
        will modify towers according to ability
        :param towers: list
        :return: None
        """
        effected = []
        for tower in towers:
            tower_x, tower_y = tower.x, tower.y

            dis = math.sqrt((self.x - tower_x) ** 2 + (self.y - tower_y) ** 2)

            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.original_range + round(tower.range * self.effect[self.level - 1])


"""damage_imgs = []
for index in range(3, 5):
    damage_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("../game_assets/towers/support tower/2",
                                                                             "support_tower_1("
                                                                             + str(index) + ").png")), (100, 100)))"""
damage_imgs = ImageCollection("../game_assets/towers/support tower/2/", 3, 1, 100, 0, "support_tower_1_")
damage_imgs.download_tower()


class DamageTower(RangeTower):
    """
    Add damage for surround towers
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 75
        self.tower_imgs = damage_imgs.images[:]
        self.effect = [0.2, 0.4]
        self.width = self.height = 100
        self.name = "damage"
        self.price = 1000

    def support(self, towers):
        """
        Will modify towers according to ability
        :param towers: list
        :return: None
        """
        effected = []
        for tower in towers:
            tower_x, tower_y = tower.x, tower.y

            dis = math.sqrt((self.x - tower_x) ** 2 + (self.y - tower_y) ** 2)

            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.original_damage + round(tower.damage * self.effect[self.level - 1])