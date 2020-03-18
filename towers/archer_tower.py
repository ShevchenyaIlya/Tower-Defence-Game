import pygame
from towers.tower import Tower
import os
import math
from menu.menu import Menu
from towers.image_collection import ImageCollection, ControlImageCollection

menu_bg = ControlImageCollection("../game_assets/menu1.png", 150, 75).download_image()
upgrade_btn = ControlImageCollection("../game_assets/upgrade.png", 50, 50).download_image()

tower_imgs = ImageCollection("../game_assets/towers/archer tower/1/", 3, 1, 100, 0, "archer_tower_2_")
tower_imgs.download_tower()

archer_imgs = ImageCollection("../game_assets/towers/archer/1/", 6, 1, 44, 0, "archer_animation_")
archer_imgs.download_tower()


class ArcherTowerLong(Tower):
    is_game_pause = True

    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs.images[:]
        self.archer_imgs = archer_imgs.images[:]
        self.archer_count = 0
        self.price = 500
        self.range = 150
        self.original_range = self.range

        self.in_range = False
        self.left = False
        self.damage = 2
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.paused = False
        self.name = "archer_long"

        # define menu and buttons
        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, 5000, "Max"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def get_upgrade_cost(self):
        """
        Gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        Draw the archer tower and animated archer
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)

        if self.in_range and not self.moving and not ArcherTowerLong.is_game_pause:
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * 10:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 10]
        win.blit(archer, (self.x - 22, self.y - archer.get_height() - 18))

    def change_range(self, r):
        """
        Change range for archer tower
        :param r: int
        :return: None
        """
        self.range -= r

    def attack(self, enemies):
        """
        Attacks an enemy in the enemy list, modifies the list
        :param enemies: list of enemies
        :return: None
        """
        money = 0
        self.in_range = False
        enemy_closest = []

        for enemy in enemies:
            enemy_x, enemy_y = enemy.x, enemy.y

            dis = math.sqrt((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2)
            if dis < self.range:
                self.in_range = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.health)
        # enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archer_count == 50:
                if first_enemy.hit(self.damage):
                    money = first_enemy.money * 2
                    # enemies.remove(first_enemy)
                    first_enemy.is_die = True

            if first_enemy.x < self.x and not self.left:
                self.left = True
                for index, img in enumerate(self.archer_imgs):
                    self.archer_imgs[index] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x > self.x:
                self.left = False
                for index, img in enumerate(self.archer_imgs):
                    self.archer_imgs[index] = pygame.transform.flip(img, True, False)

        return money


# load short archer tower images
tower_imgs_sibling = ImageCollection("../game_assets/towers/archer tower/2/", 3, 1, 100, 0, "archer_tower_2_")
tower_imgs_sibling.download_tower()

archer_imgs_sibling = ImageCollection("../game_assets/towers/archer/2/", 6, 1, 44, 0, "archer_animation_")
archer_imgs_sibling.download_tower()


class ArcherTowerShort(ArcherTowerLong):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs_sibling.images[:]
        self.archer_imgs = archer_imgs_sibling.images[:]
        self.archer_count = 0
        self.range = 120
        self.price = 750
        self.original_range = self.range
        self.in_range = False
        self.left = False
        self.damage = 4
        self.original_damage = self.damage
        self.width = self.height = 100
        self.name = "archer_short"

        # define menu and buttons
        self.menu = Menu(self, self.x, self.y, menu_bg, [2500, 5500, "Max"])
        self.menu.add_btn(upgrade_btn, "Upgrade")


