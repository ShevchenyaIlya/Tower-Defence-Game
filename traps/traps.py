import pygame
from game.image_collection import ControlImageCollection

trap = ControlImageCollection("../game_assets/traps_icon_3.png", 60, 55).download_image()
trap1 = ControlImageCollection("../game_assets/traps_1.png", 80, 80).download_image()
trap2 = ControlImageCollection("../game_assets/traps_2.png", 80, 80).download_image()


class Trap:
    def __init__(self, x, y, img):
        self.x = x + img.get_width() / 2
        self.y = y + img.get_height() / 2
        self.img = img
        self.animation = []
        self.health = 0
        self.damage = 0
        self.max_health = 10
        self.cost = 0
        self.name = None
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.place_color = (0, 255, 0, 100)
        self.is_attacked = False
        self.is_destroyed = False
        self.animation_count = 0

    def draw(self, win):
        """
        Draw trap depending of it modification
        :param win: surface
        :return: None
        """
        if self.is_destroyed:
            self.img = self.animation[self.animation_count // 2]
            win.blit(self.img, (self.x, self.y))
        else:
            win.blit(self.img, (self.x, self.y))
            if self.is_attacked:
                self.draw_health_bar(win)

    def move(self, x, y):
        """
        Move trap, by changing coordinates
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x - self.width / 2
        self.y = y - self.height / 2

    def draw_placement(self, win):
        """
        Draw circle, that show if you can place trap in current position
        :param win: surface
        :return: None
        """
        surface = pygame.Surface((45 * 2, 45 * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (45, 45), 35, 0)
        win.blit(surface, (self.x - self.width // 2 + 35, self.y - self.height // 2 + 35))

    def stop_enemy(self, enemies):
        """
        Stop enemy animation if they collide with each other
        :param enemies: list
        :return: None
        """
        for enemy in enemies:
            if self.x + self.width // 2 - 28 <= enemy.x <= self.x + self.width // 2 + 35 and self.y + self.height // 2 - 40 <= enemy.y <= self.y + self.height // 2 + 40:
                enemy.to_stopped_by_trap(self)

    def hit(self, damage):
        """
        Make damage for trap, by subtracting enemy damage from trap health
        :param damage: int
        :return: boolean
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def draw_health_bar(self, win):
        """
        Draw trap health bar if enemy hit her
        :param win: surface
        :return: None
        """
        length = 50
        if self.health > 0:
            move_by = length / self.max_health
            health_bar = round(move_by * self.health)
        else:
            health_bar = 0

        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y + self.height - 15, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y + self.height - 15, health_bar, 10), 0)

    def destroy(self, traps, enemies):
        self.animation_count += 1
        if self.animation_count >= len(self.animation) * 2:
            self.animation_count = 0
            for enemy in enemies:
                if self.x + self.width // 2 - 28 <= enemy.x <= self.x + self.width // 2 + 35 and self.y + self.height // 2 - 40 <= enemy.y <= self.y + self.height // 2 + 40:
                    if enemy.hit(self.damage):
                        enemy.to_dying()
            traps.remove(self)


class StopTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap1)
        self.name = "stop_trap"
        self.cost = 150
        self.max_health = 75
        self.health = self.max_health


class KillTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap)
        self.name = "kill_trap"
        self.max_health = 35
        self.health = self.max_health


destroy = []
for i in range(1, 9):
    destroy.append(pygame.transform.scale(pygame.image.load("../game_assets/trap_animations/1/1_trap_1_die_" + str(i) + ".png"), (100, 100)))


class DestroyTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap2)
        self.name = "destroy_trap"
        self.cost = 200
        self.damage = 10
        self.max_health = 35
        self.health = self.max_health
        self.animation = destroy[:]
