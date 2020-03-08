from towers.image_collection import ControlImageCollection

trap = ControlImageCollection("../game_assets/traps_icon_3.png", 60, 55).download_image()
trap1 = ControlImageCollection("../game_assets/traps_1.png", 80, 80).download_image()
trap2 = ControlImageCollection("../game_assets/traps_2.png", 80, 80).download_image()


class Trap:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class StopTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap2)


class KillTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap)


class DestroyingTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, trap)