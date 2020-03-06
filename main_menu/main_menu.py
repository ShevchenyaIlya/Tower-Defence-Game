import pygame
import os
from towers.game import Game
from towers.image_collection import ControlImageCollection


"""start_btn = pygame.transform.scale(pygame.image.load(os.path.join("../game_assets", "start_menu_button.png")), (250, 350))
logo = pygame.transform.scale(pygame.image.load(os.path.join("../game_assets", "game_logo_1.png")), (1000, 250))"""
start_btn = ControlImageCollection("../game_assets/start_menu_button.png", 250, 350).download_image()
logo = ControlImageCollection("../game_assets/game_logo_1.png", 1000, 250).download_image()


class MainMenu:
    def __init__(self):
        self.__width = 1250
        self.__height = 700
        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.bg = pygame.image.load(os.path.join("../game_assets/hole_backgrounds.png"))
        self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        self.__btn = (self.__width / 2 - start_btn.get_width() / 2, 350, start_btn.get_width(), start_btn.get_height())
        self.__text_font = pygame.font.SysFont("life count", 170)

    def run(self):
        run = True
        game_quit = False

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    if self.__btn[0] <= x <= self.__btn[0] + self.__btn[2]:
                        if self.__btn[1] <= y <= self.__btn[1] + self.__btn[3]:
                            game = Game(self.__win)
                            game.run()
                            del game
                            game_quit = True
                            run = False
                            break
            if not game_quit:
                self.draw()

    def draw(self):
        self.__win.blit(self.bg, (0, 0))
        self.__win.blit(start_btn, (self.__btn[0], self.__btn[1]))
        self.__win.blit(logo, (self.__width / 2 - logo.get_width() / 2, 5))
        pygame.display.update()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
