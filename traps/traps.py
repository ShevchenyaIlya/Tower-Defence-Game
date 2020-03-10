import pygame
from towers.image_collection import ControlImageCollection

trap = ControlImageCollection("../game_assets/traps_icon_3.png", 60, 55).download_image()
trap1 = ControlImageCollection("../game_assets/traps_1.png", 80, 80).download_image()
trap2 = ControlImageCollection("../game_assets/traps_2.png", 80, 80).download_image()


class Trap:
    def __init__(self, x, y, img):
        self.x = x - img.get_width() / 2
        self.y = y - img.get_height() / 2
        self.img = img
        self.health = 0
        self.max_health = 10
        self.cost = 0
        self.name = None
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.place_color = (0, 255, 0, 100)
        self.is_attacked = False

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        if self.is_attacked:
            self.draw_health_bar(win)

    def move(self, x, y):
        self.x = x - self.width / 2
        self.y = y - self.height / 2

    def draw_placement(self, win):
        surface = pygame.Surface((45 * 2, 45 * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (45, 45), 35, 0)
        win.blit(surface, (self.x - self.width // 2 + 35, self.y - self.height // 2 + 35))

    def stop_enemy(self, enemies):
        for enemy in enemies:
            if self.x + self.width // 2 - 28 <= enemy.x <= self.x + self.width // 2 + 35 and self.y + self.height // 2 - 40 <= enemy.y <= self.y + self.height // 2 + 40:
                enemy.stop_by_trap = self

    def hit(self, damage):
        print(self.health)
        print("hit")
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def draw_health_bar(self, win):
        length = 50
        if self.health > 0:
            move_by = length / self.max_health
            health_bar = round(move_by * self.health)
        else:
            health_bar = 0

        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y + self.height - 15, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y + self.height - 15, health_bar, 10), 0)


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


class DestroyTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap2)
        self.name = "destroy_trap"
        self.cost = 200
