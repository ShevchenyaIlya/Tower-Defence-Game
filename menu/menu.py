import pygame
from towers.control_object import ButtonObject, MenuObject
from towers.interfaces import ILocation
from towers.image_collection import ControlImageCollection


big_star = ControlImageCollection("../game_assets/star1.png", 50, 50).download_image()
small_star = ControlImageCollection("../game_assets/star1.png", 36, 36).download_image()


class Button(ButtonObject, ILocation):
    """
    Button class for menu objects
    """
    def __init__(self, menu, img, name):
        super().__init__()
        self.name = name
        self.img = img
        self.x = menu.x - 50
        self.y = menu.y - 105
        self.menu = menu
        self.item_cost = []
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, x, y):
        """
        return true if the user has collided with the menu
        :param x: int
        :param y: int
        :return: bool
        """
        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                return True
        return False

    def update(self):
        """
        Updates button position
        :return: None
        """
        self.x = self.menu.x - 50
        self.y = self.menu.y - 105

    def draw(self, win):
        """
        Just draw the button in position(x, y)
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x, self.y))

    def get_position(self):
        return self.x, self.y


class Menu(MenuObject, ILocation):
    """
    menu for holding items
    """
    def __init__(self, tower, x, y, img, item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.items = 0
        self.item_cost = item_cost
        self.buttons = []
        self.bg = img
        self.font = pygame.font.SysFont("conicsans", 25)
        self.tower = tower

    def add_btn(self, img, name):
        """
        Add button to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))

    def draw(self, win):
        """
        Draws buttons and menu background
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width() / 2, self.y - 120))
        for item in self.buttons:
            item.draw(win)
            win.blit(big_star, (item.x + item.width + 3, item.y - 3))
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255, 255, 255))
            win.blit(text, (item.x + item.width + 32 - text.get_width() / 2, item.y + big_star.get_height() - 17))

    def get_item_cost(self):
        """
        Gets cost of tower upgrade to the next level
        :return: int
        """
        return self.item_cost[self.tower.level - 1]

    def get_clicked(self, x, y):
        """
        return the clicked item from the menu
        :param x: int
        :param y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(x, y):
                return btn.name

        return None

    def update(self):
        """
        Update menu and button location
        :return: None
        """
        for btn in self.buttons:
            btn.update()

    def get_position(self):
        return self.x, self.y


class PlayPauseButton(Button):
    def __init__(self, play_img, pause_image, x, y):
        self.img = play_img
        self.play_img = play_img
        self.pause_img = pause_image
        self.x = x
        self.y = y
        self.item_cost = []
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pause = True
        self.font = pygame.font.SysFont("conicsans", 23)

    def draw(self, win):
        if self.pause:
            win.blit(self.play_img, (self.x, self.y))
        else:
            win.blit(self.pause_img, (self.x, self.y))


class VerticalButton(Button):
    """
    Button class for menu objects
    """
    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.item_cost = []
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost


class VerticalMenu(Menu):
    """
    Vertical menu for side bar of game
    """
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.items = 0
        self.buttons = []
        self.bg = img
        self.font = pygame.font.SysFont("conicsans", 25)

    def add_btn(self, img, name, cost):
        """
        Add button to vertical menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.items += 1
        btn_x = self.x - 30
        btn_y = self.y - 30 + (self.items - 1) * 120
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

    def draw(self, win):
        """
        Draws buttons and menu background
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width() / 2, self.y - 110))
        for item in self.buttons:
            VerticalButton.draw(item, win)
            win.blit(small_star, (item.x + item.width // 2 + 2, item.y + item.height - 20))
            text = self.font.render(str(item.cost), 1, (255, 255, 255))
            win.blit(text, (item.x - text.get_width() // 2 + 20, item.y + small_star.get_height() + 21))

    def get_item_cost(self, name):
        """
        gets cost of items
        :param name: str
        :return: int
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1
