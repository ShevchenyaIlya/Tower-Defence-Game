import pygame
from menu.menu import Menu
import math
from game.positional_object import PositionalObject
from game.interfaces import ILocation, IUpgradable
from game.image_collection import ControlImageCollection


menu_background = ControlImageCollection("../game_assets/menu1.png", 150, 75).download_image()
button_background = ControlImageCollection("../game_assets/upgrade.png", 50, 50).download_image()


class Tower(PositionalObject, ILocation, IUpgradable):
    """
    Abstract class for towers
    """
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.price = 0
        self.level = 1
        self.range = 0
        self.selected = False
        self.is_collide = False

        # define menu and buttons
        self.menu = Menu(self, self.x, self.y, menu_background, [2000, "Max"])
        self.menu.add_btn(button_background, "Upgrade")

        self.tower_imgs = []
        self.damage = 1
        self.sell_price = []

        self.place_color = (0, 255, 0, 100)

    def get_position(self):
        return self.x, self.y

    def draw(self, win):
        """
        Draws the tower
        :param win: surface
        :return: None
        """
        img = self.tower_imgs[self.level - 1]
        win.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))

        # draw menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self, win):
        if self.selected:
            # Draw range circle
            surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)
            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):
        surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (45, 45), 45, 0)
        win.blit(surface, (self.x - 45, self.y - 45))

    def click(self, x, y):
        """
        Returns if tower has been clicked on
        and selects tower if it was clicked
        :param x: int
        :param y: int
        :return: bool
        """
        img = self.tower_imgs[self.level - 1]
        if self.x - img.get_width() // 2 <= x <= self.x + self.width - img.get_width() // 2:
            if self.y - img.get_height() // 2 <= y <= self.y + self.height - img.get_height() // 2:
                return True
        return False

    def sell(self):
        """
        Call to sell the tower, returns sell cost
        :return: int
        """

        return self.sell_price[self.level - 1]

    def get_upgrade_cost(self):
        """
        Return the upgrade cost, if 0 then can't upgrade anymore
        :return:
        """
        return self.price

    def upgrade(self):
        """
        Upgrades the tower for given cost
        :return: None
        """
        if self.level < len(self.tower_imgs):
            self.level += 1
            self.damage += 1

    def move(self, x, y):
        """
        Moves tower to given x and y position
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

    def collide(self, other_tower):
        x2 = other_tower.x
        y2 = other_tower.y

        dis = math.sqrt((x2 - self.x) ** 2 + (y2 - self.y) ** 2)
        if dis >= 90:
            return False
        else:
            return True
