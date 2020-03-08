import pygame
import math
from towers.positional_object import PositionalObject
from towers.interfaces import ILocation, IMovable


class Enemy(PositionalObject, ILocation, IMovable):
    def __init__(self):
        super().__init__()
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(-10, 225), (14, 224), (165, 225), (216, 252), (269, 282), (555, 284), (619, 248), (639, 179),
                     (687, 74), (750, 52), (813, 70), (852, 116), (870, 187), (911, 257), (983, 276), (1055, 308),
                     (1082, 385), (1071, 454), (1019, 496), (797, 501), (715, 543), (412, 554), (163, 548), (98, 484),
                     (81, 393), (18, 339), (-30, 335)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.img = None
        self.dis = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0
        self.speed_increase = 1.2

    def get_position(self):
        return self.x, self.y

    def draw(self, win):
        """
        Draws the enemy with given images
        :param win: surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]

        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 2 - 35))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(win, (255, 0, 0), (self.x - 30, self.y - 75, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 30, self.y - 75, health_bar, 10), 0)

    def collide(self, x, y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y: int
        :return: Bool
        """

        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                return True
        return False

    def move(self):
        """
        Move enemy
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length * self.speed_increase, dirn[1] / length * self.speed_increase)  # mul increase the speed

        if dirn[0] < 0 and not self.flipped:
            self.flipped = True
            for index, img in enumerate(self.imgs):
                self.imgs[index] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Go to the next point
        if dirn[0] >= 0:  # Moving right
            if dirn[1] >= 0:  # Moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # Moving left
            if dirn[1] <= 0:  # Moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1

    def hit(self, damage):
        """
        Return if an enemy has died and removes one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False
