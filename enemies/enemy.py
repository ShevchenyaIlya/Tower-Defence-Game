import pygame
import math

from game.positional_object import PositionalObject
from game.interfaces import ILocation, IMovable
from map.game_map import Map


class States:
    ACTIVE = 'active'
    STOPPED_BY_TRAP = 'stopped_by_trap'
    DYING = 'dying'


class Enemy(PositionalObject, ILocation, IMovable):
    def __init__(self, path, game_map):
        super().__init__()
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.armor = 0
        self.magick_resist = 0
        self.damage = 0
        self.vel = 3
        self.path = path
        self.game_map = game_map

        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.img = None
        self.dis = 0
        self.move_count = 0
        self.move_dis = 0
        self.state = States.ACTIVE
        self.active_imgs = []
        self.attack_imgs = []
        self.die_imgs = []

        self.flipped = False
        self.max_health = 0
        self.speed_increase = 1.2
        self.stop_by_trap = None

    def get_position(self):
        """
        Return actual position of enemy
        :return: tuple
        """
        return self.x, self.y

    @property
    def is_die(self):
        return self.state == States.DYING

    @property
    def is_stopped_by_trap(self):
        return self.state == States.STOPPED_BY_TRAP

    @property
    def is_active(self):
        return self.state == States.ACTIVE

    @property
    def imgs(self):
        return {
            States.ACTIVE: self.active_imgs,
            States.STOPPED_BY_TRAP: self.attack_imgs,
            States.DYING: self.die_imgs,
        }[self.state]

    def to_active(self):
        if self.is_die:
            return
        self.stop_by_trap = None
        self.state = States.ACTIVE

    def to_stopped_by_trap(self, trap):
        if self.is_die:
            return 
        self.stop_by_trap = trap
        self.state = States.STOPPED_BY_TRAP

    def to_dying(self):
        self.stop_by_trap = None
        self.state = States.DYING

    def draw(self, win):
        """
        Draws the enemy with given images
        :param win: surface
        :return: None
        """
        self.img = self.imgs[self.animation_count // 2]

        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 2 - 35))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        if self.health > 0:
            move_by = length / self.max_health
            health_bar = round(move_by * self.health)
        else:
            health_bar = 0

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

    def flip_images(self):
        """
        Flip all images when enemy rotates
        :return: None
        """
        for index, img in enumerate(self.active_imgs):
            self.active_imgs[index] = pygame.transform.flip(img, True, False)
        for index, img in enumerate(self.attack_imgs):
            self.attack_imgs[index] = pygame.transform.flip(img, True, False)
        for index, img in enumerate(self.die_imgs):
            self.die_imgs[index] = pygame.transform.flip(img, True, False)

    def move(self):
        """
        Move enemy
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.active_imgs) * 2:
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            if self.game_map == Map.FIRST_MAP:
                x2, y2 = (-10, 355)
            elif self.game_map == Map.SECOND_MAP:
                x2, y2 = (1250, 730)
            elif self.game_map == Map.THIRD_MAP:
                x2, y2 = (784, 730)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length * self.speed_increase, dirn[1] / length * self.speed_increase)  # mul increase the speed

        if dirn[0] < 0 and not self.flipped:
            self.flipped = True
            self.flip_images()
        elif dirn[0] > 0 and self.flipped:
            self.flipped = False
            self.flip_images()

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
        self.health -= damage - (self.armor / 4 + self.magick_resist / 4)
        if self.health <= 0:
            return True
        return False

    def animate_attack(self):
        """
        Works if enemy collide with trap
        Just change animation from run to attack and continue image cycle going
        :return: None
        """
        self.animation_count += 1
        self.stop_by_trap.is_attacked = True
        if self.animation_count >= len(self.attack_imgs) * 2:
            self.animation_count = 0

    def animate_die(self, enemies):
        """
        Continue animate enemy if they die
        Play animation for last image and remove enemy
        :param enemies: list
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.die_imgs) * 2:
            self.animation_count = 0
            enemies.remove(self)
            return True

    def attack(self, traps):
        """
        Attack trap if enemy collide with this trap
        :param traps: list
        :return: None
        """
        if self.stop_by_trap in traps:
            if self.animation_count == 19:
                if self.stop_by_trap.hit(self.damage):
                    if self.stop_by_trap.name == "destroy_trap":
                        self.stop_by_trap.is_destroyed = True
                    else:
                        traps.remove(self.stop_by_trap)
                    self.to_active()
                    self.animation_count = 0
        else:
            self.to_active()



