import pygame
import os
import sqlite3
import string
import time
import datetime
from towers.game import Game
from towers.image_collection import ControlImageCollection

# Создание таблицы
conn = sqlite3.connect("tower_defence_database.db")
cursor = conn.cursor()

cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='information' ''')

top_five = []
if cursor.fetchone()[0] == 0:
    cursor.execute("""CREATE TABLE information (username text, wave text, enemy_kill text, last_entrance text,
                      lives text, money text, result text, spend_time text)""")

cursor.execute("SELECT * FROM information")
db_rows = cursor.fetchall()
db_rows.sort(key=lambda x: x[1], reverse=True)

if len(db_rows) < 6:
    iter_number = len(db_rows)
else:
    iter_number = 6

for row in range(iter_number):
    top_five.append((db_rows[row][0], db_rows[row][1], db_rows[row][2]))


start_btn = ControlImageCollection("../game_assets/start_menu_button.png", 250, 350).download_image()
logo = ControlImageCollection("../game_assets/game_logo_1.png", 1000, 250).download_image()
panel = ControlImageCollection("../game_assets/brown-wood.png", 425, 300).download_image()
line = ControlImageCollection("../game_assets/vertical_menu_1.png", 450, 85).download_image()
text_background = ControlImageCollection("../game_assets/menu1.png", 425, 85).download_image()

label_font = pygame.font.SysFont("username", 45)


class MainMenu:
    def __init__(self):
        self.__width = 1250
        self.__height = 700
        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.bg = pygame.image.load(os.path.join("../game_assets/hole_backgrounds.png"))
        self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        self.__btn = (self.__width / 2 - start_btn.get_width() / 2, 350, start_btn.get_width(), start_btn.get_height())
        self.__text_font = pygame.font.SysFont("username", 50)
        self.__score_font = pygame.font.SysFont("monospace", 20, 1)
        self.__username = ""
        self.__superuser_name = "TDgamecreator"
        self.start_input = False

    def run(self):
        run = True
        game_quit = False

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.start_input = not self.start_input

                    if self.start_input:
                        pressed_keys = event.dict['unicode']

                        if event.key == pygame.K_BACKSPACE:
                            self.__username = self.__username[:-1]

                        if pressed_keys in string.ascii_letters or pressed_keys in string.digits:
                            if len(self.__username) <= 13:
                                self.__username += pressed_keys

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    # Activate username input
                    if self.__width / 2 + 140 <= x <= self.__width / 2 + 590:
                        if self.__height / 2 + 50 <= y <= self.__height / 2 + 135:
                            self.start_input = True
                        else:
                            self.start_input = False
                    else:
                        self.start_input = False

                    if self.__username:
                        if self.__btn[0] <= x <= self.__btn[0] + self.__btn[2]:
                            if self.__btn[1] <= y <= self.__btn[1] + self.__btn[3]:
                                game = Game(self.__win)

                                before_interruption = 0
                                for index, row in enumerate(db_rows):
                                    if self.__username == row[0] and row[6] == "interrupted":
                                        game.money = int(row[5])
                                        game.wave = int(row[1])
                                        game.lives = int(row[4])
                                        game.enemy_kill = int(row[2])
                                        before_interruption = float(row[7])

                                        cursor.execute("DELETE FROM information WHERE username=? AND result=? AND wave=? AND money=? AND lives=? AND enemy_kill = ?;", (self.__username, "interrupted", row[1], row[5], row[4], row[2]))
                                        conn.commit()
                                        break

                                if self.__username == self.__superuser_name:
                                    game.money = 100000000000
                                    game.lives = 100000000000

                                start_timer = time.time()
                                res = game.run()
                                spend_time = time.time() - start_timer + before_interruption

                                if res is None:
                                    game_result = "interrupted"
                                elif res:
                                    game_result = "win"
                                else:
                                    game_result = "lose"

                                if self.__username != self.__superuser_name:
                                    write_data = [self.__username, game.wave, game.enemy_kill,
                                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), game.lives,
                                                  game.money, game_result, spend_time]
                                    cursor.execute("""INSERT INTO information VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", write_data)
                                    conn.commit()

                                if res is None:
                                    del game
                                    game_quit = True
                                    run = False
                                    break
                                elif res:
                                    del game
                                    win_or_lose = WinOrLose()
                                    win_or_lose.win = True
                                    game_quit = True
                                    if win_or_lose.run():
                                        run = True
                                    else:
                                        run = False
                                        break
                                elif not res:
                                    del game
                                    win_or_lose = WinOrLose()
                                    win_or_lose.win = False
                                    game_quit = True
                                    if win_or_lose.run():
                                        run = True
                                    else:
                                        run = False
                                        break
            if not game_quit:
                self.draw()

    def draw(self):
        self.__win.blit(self.bg, (0, 0))
        self.__win.blit(start_btn, (self.__btn[0], self.__btn[1]))
        self.__win.blit(logo, (self.__width / 2 - logo.get_width() / 2, 5))

        # Right table elements
        self.__win.blit(panel, (self.__width / 2 + 150, self.__height / 2 - 50))
        self.__win.blit(text_background, (self.__width / 2 + 150, self.__height / 2 - 50))
        self.__win.blit(line, (self.__width / 2 + 140, self.__height / 2 + 50))
        text = self.__text_font.render("Choose username", 1, (0, 0, 0))
        self.__win.blit(text, (self.__width * 3/4 - 100, self.__height / 2 - 25))
        username = label_font.render(self.__username, 1, (0, 0, 0))
        self.__win.blit(username, (self.__width / 2 + 200, self.__height / 2 + 80))

        # Left table elements
        # TODO: read users from database with their scores
        self.__win.blit(panel, (50, self.__height / 2 - 50))
        score_table = self.__text_font.render("Score", 1, (0, 0, 0))
        self.__win.blit(text_background, (50, self.__height / 2 - 50))
        self.__win.blit(score_table, (225, self.__height / 2 - 25))

        self.draw_scores()
        pygame.display.update()

    def draw_scores(self):

        best_score = self.__score_font.render(("Nickname:" + "      " + "Wave:" + "   " + "Enemy kill:"), 1, (0, 0, 0))
        self.__win.blit(best_score, (65, self.__height / 2 + 30))

        for row in range(iter_number):
            space_number = (17 - len(top_five[row][0]), 10 - len(top_five[row][1]))
            best_score = self.__score_font.render((top_five[row][0] + " " * space_number[0] + top_five[row][1] + " " * space_number[1] + top_five[row][2]), 1, (0, 0, 0))
            self.__win.blit(best_score, (65, self.__height / 2 + 30 + 30 * (row + 1)))


win_logo = ControlImageCollection("../game_assets/you_win.png", 1000, 250).download_image()
lose_logo = ControlImageCollection("../game_assets/you_lose.png", 1000, 250).download_image()


class WinOrLose:
    def __init__(self):
        self.__width = 1250
        self.__height = 700
        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.bg = pygame.image.load(os.path.join("../game_assets/hole_backgrounds.png"))
        self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        self.__btn = (self.__width / 2 - start_btn.get_width() / 2, 350, start_btn.get_width(), start_btn.get_height())
        self.__text_font = pygame.font.SysFont("life count", 120)
        self.win_logo = win_logo
        self.lose_logo = lose_logo
        self.win = False

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    if self.__btn[0] <= x <= self.__btn[0] + self.__btn[2]:
                        if self.__btn[1] <= y <= self.__btn[1] + self.__btn[3]:
                            return True

            self.draw()

    def draw(self):
        self.__win.blit(self.bg, (0, 0))
        if self.win:
            self.__win.blit(self.win_logo, (self.__width / 2 - logo.get_width() / 2, 5))
        else:
            self.__win.blit(self.lose_logo, (self.__width / 2 - logo.get_width() / 2, 5))

        text = self.__text_font.render("Play again?", 1, (0, 0, 0))
        self.__win.blit(text, (self.__width / 2 - text.get_width() // 2, 250))
        self.__win.blit(start_btn, (self.__btn[0], self.__btn[1]))

        """self.__win.blit(panel, (50, self.__height / 2 - 50))
        score_table = label_font.render("Score", 1, (0, 0, 0))
        self.__win.blit(text_background, (50, self.__height / 2 - 50))
        self.__win.blit(score_table, (225, self.__height / 2 - 25))"""
        pygame.display.update()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
