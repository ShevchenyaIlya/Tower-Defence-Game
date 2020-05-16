import pygame
import os
import sqlite3
import string
import time
import datetime

from game.game import Game
from game.image_collection import ControlImageCollection
from map.game_map import Map

# TODO: Add map classification to database
# TODO: Change lose/win screen

# Создание таблицы
conn = sqlite3.connect("tower_defence_database.db")
cursor = conn.cursor()

cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='information1' ''')


if cursor.fetchone()[0] == 0:
    cursor.execute("""CREATE TABLE information1 (username text, wave text, enemy_kill text, last_entrance text,
                      lives text, money text, result text, spend_time text, map text)""")

cursor.execute("SELECT * FROM information1")
db_rows = cursor.fetchall()
db_rows.sort(key=lambda x: int(x[1]), reverse=True)


def get_db_rows(row_count):
    """
    Get score results as rows from database
    :param row_count: int
    :return: tuple
    """

    top_db_rows = []
    if len(db_rows) < row_count:
        iter_number = len(db_rows)
    else:
        iter_number = row_count

    for row in range(iter_number):
        top_db_rows.append((db_rows[row][0], db_rows[row][1], db_rows[row][2]))

    return top_db_rows, iter_number


top_six, item_number_6 = get_db_rows(6)
top_eleven, item_number_11 = get_db_rows(11)

start_btn = ControlImageCollection("../game_assets/start_menu_button.png", 250, 350).download_image()
logo = ControlImageCollection("../game_assets/game_logo_1.png", 1000, 250).download_image()
choose_map_logo = ControlImageCollection("../game_assets/choose_game_logo.png", 1000, 250).download_image()
play_again_logo = ControlImageCollection("../game_assets/play_again_logo.png", 300, 100).download_image()
coming_soon_logo = pygame.transform.rotate(
    ControlImageCollection("../game_assets/coming_soon_logo.png", 250, 75).download_image(), 45)
panel = ControlImageCollection("../game_assets/brown-wood.png", 425, 300).download_image()
panel_modified = ControlImageCollection("../game_assets/brown-wood.png", 425, 500).download_image()
line = ControlImageCollection("../game_assets/vertical_menu_1.png", 450, 85).download_image()
text_background = ControlImageCollection("../game_assets/menu1.png", 425, 85).download_image()
win_logo = ControlImageCollection("../game_assets/you_win.png", 600, 150).download_image()
lose_logo = ControlImageCollection("../game_assets/you_lose.png", 600, 150).download_image()
label_font = pygame.font.SysFont("username", 45)


class GameResult:
    """Class for two states such as WIN/LOSE"""
    WIN = True
    LOSE = False


class MainMenu:
    def __init__(self):
        self.__width = 1250
        self.__height = 700
        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.bg = pygame.image.load(os.path.join("../game_assets/hole_backgrounds.png"))
        self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        self.__btn = (self.__width / 2 - start_btn.get_width() / 2, 350, start_btn.get_width(), start_btn.get_height())
        self.__big_text_font = pygame.font.SysFont("username", 80)
        self.__text_font = pygame.font.SysFont("username", 50)
        self.__score_font = pygame.font.SysFont("monospace", 20, 1)
        self.__username = ""
        self.__superuser_name = "TDgamecreator"
        self.start_input = False
        self.__choose_map = False
        self.__activate_game = False
        self.win_or_lose = False
        self.game_result = None
        self.attempt = 0
        self.user_score = None
        self.game_map = Map.FIRST_MAP
        self.notification_position = -100

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

                    if self.__username and event.key == 13:
                        self.__choose_map = True

                    if self.start_input:
                        pressed_keys = event.dict['unicode']
                        if event.key == pygame.K_BACKSPACE:
                            self.__username = self.__username[:-1]

                        if pressed_keys in string.ascii_letters or pressed_keys in string.digits:
                            if len(self.__username) <= 13:
                                self.__username += pressed_keys

                if event.type == pygame.MOUSEMOTION:
                    if not self.win_or_lose:
                        x, y = pygame.mouse.get_pos()
                        if self.__choose_map:
                            if x <= self.__width / 2 and y <= self.__height / 2:
                                self.game_map = Map.THIRD_MAP
                            elif x > self.__width / 2 and y <= self.__height / 2:
                                self.game_map = Map.FIRST_MAP
                            elif x <= self.__width / 2 and y > self.__height / 2:
                                self.game_map = Map.SECOND_MAP
                            elif x > self.__width / 2 and y > self.__height / 2:
                                self.game_map = Map.FOURTH_MAP

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    if not self.win_or_lose:
                        if not self.__choose_map:
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
                                        self.__choose_map = True
                        else:
                            if self.game_map == Map.FIRST_MAP\
                                    or self.game_map == Map.SECOND_MAP\
                                    or self.game_map == Map.THIRD_MAP\
                                    or self.game_map == Map.FOURTH_MAP:
                                self.__activate_game = True
                    else:
                        if self.__btn[0] + self.__width / 4 <= x <= self.__btn[0] + self.__btn[2] + self.__width / 4:
                            if self.__btn[1] <= y <= self.__btn[1] + self.__btn[3]:
                                self.__activate_game = True

                if self.__activate_game:
                    game = Game(self.__win, self.__username)
                    game.set_game_map(self.game_map)

                    if not self.attempt:
                        before_interruption = 0
                        for index, row in enumerate(db_rows):
                            if self.__username == row[0] and row[6] == "interrupted":
                                saved_map = str(row[8])
                                game_map = ""

                                if saved_map == 'desert':
                                    game_map = Map.FIRST_MAP
                                elif saved_map == 'hell':
                                    game_map = Map.SECOND_MAP
                                elif saved_map == 'forest':
                                    game_map = Map.THIRD_MAP
                                elif saved_map == 'winter':
                                    game_map = Map.FOURTH_MAP

                                if self.game_map == game_map:
                                    game.money = int(row[5])
                                    game.wave = int(row[1])
                                    game.lives = int(row[4])
                                    game.enemy_kill = int(row[2])
                                    before_interruption = float(row[7])

                                    cursor.execute(
                                        "DELETE FROM information1 WHERE username=? \
                                        AND result=? AND wave=? AND money=? AND lives=? AND enemy_kill=? AND map=?;",
                                        (self.__username, "interrupted", row[1], row[5], row[4], row[2], game_map))
                                    conn.commit()
                                    break

                        if self.__username == self.__superuser_name:
                            game.money = 100000000000
                            game.lives = 100000000000

                    start_timer = time.time()
                    game_result = game.run()
                    spend_time = time.time() - start_timer + before_interruption

                    if game_result is None:
                        game_result_status = "interrupted"
                    elif game_result:
                        game_result_status = "win"
                    else:
                        game_result_status = "lose"

                    if self.__username != self.__superuser_name:
                        write_data = [self.__username, game.wave, game.enemy_kill,
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), game.lives,
                                      game.money, game_result_status, spend_time, self.game_map]
                        cursor.execute("""INSERT INTO information1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", write_data)
                        conn.commit()

                    if game_result is None:
                        self.restart_game(game)
                        game_quit = True
                        run = False
                        break
                    elif game_result or not game_result:
                        self.user_score = game.get_score()
                        self.restart_game(game)
                        self.win_or_lose = True
                        if game_result:
                            self.game_result = GameResult.WIN
                        else:
                            self.game_result = GameResult.LOSE

                        # game_quit = True
                        # break

                    # elif res:
                    #     self.restart_game(game)
                    #     win_or_lose = WinOrLose()
                    #     win_or_lose.win = True
                    #     game_quit = True
                    #     if win_or_lose.run():
                    #         run = True
                    #     else:
                    #         run = False
                    #         break
                    # elif not res:
                    #     self.restart_game(game)
                    #     win_or_lose = WinOrLose()
                    #     win_or_lose.win = False
                    #     game_quit = True
                    #     if win_or_lose.run():
                    #         run = True
                    #     else:
                    #         run = False
                    #         break

                    self.attempt += 1
                    self.__activate_game = False
                    self.__choose_map = False
            if not game_quit:
                self.draw()

    def draw(self):
        self.__win.blit(self.bg, (0, 0))

        if not self.win_or_lose:
            if not self.__choose_map:
                self.__win.blit(logo, (self.__width / 2 - logo.get_width() / 2, 5))
            else:
                pass
                # self.__win.blit(choose_map_logo, (self.__width / 2 - choose_map_logo.get_width() / 2, -50))

            if not self.__choose_map:
                # Draw start button
                self.__win.blit(start_btn, (self.__btn[0], self.__btn[1]))

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

                self.draw_scores(65, self.__height / 2 + 30, item_number_6, top_six)
            else:
                if self.game_map == Map.THIRD_MAP:
                    pygame.draw.rect(self.__win, (0, 128, 255, 200), (0, 0, self.__width / 2, self.__height / 2), 5)
                elif self.game_map == Map.FIRST_MAP:
                    pygame.draw.rect(self.__win, (0, 128, 255, 200), (self.__width / 2, 0,
                                                                      self.__width, self.__height / 2), 5)
                elif self.game_map == Map.SECOND_MAP:
                    pygame.draw.rect(self.__win, (0, 128, 255, 200), (0, self.__height / 2,
                                                                      self.__width / 2, self.__height), 5)
                elif self.game_map == Map.FOURTH_MAP:
                    pygame.draw.rect(self.__win, (0, 128, 255, 200), (self.__width / 2, self.__height / 2,
                                                                      self.__width, self.__height), 5)

                # self.__win.blit(coming_soon_logo, (self.__width / 4 - 150,
                #                                    self.__height * (1 / 4) - 75))
                # self.__win.blit(coming_soon_logo, (self.__width * (3 / 4) - 100,
                #                                   self.__height * (3 / 4) - 75))
        else:
            # Lose/Win screen if game ended
            # Draw win/lose logo
            if self.game_result == GameResult.WIN:
                self.__win.blit(win_logo, (self.__width / 2 - win_logo.get_width() / 2, 5))
            elif self.game_result == GameResult.LOSE:
                self.__win.blit(lose_logo, (self.__width / 2 - lose_logo.get_width() / 2, 5))

            # Draw table with personal scores from database
            self.__win.blit(panel_modified, (100, 150))
            score_table = self.__text_font.render("Score", 1, (0, 0, 0))
            self.__win.blit(text_background, (100, 150))
            self.__win.blit(score_table, (270, 180))
            best_score = self.__score_font.render("Your personal score", 1, (0, 0, 0))
            self.__win.blit(best_score, (115, 230))
            space_number = (17 - len(self.__username), 10 - len(str(self.user_score[0])))
            your_score = self.__score_font.render((self.__username + " " * space_number[0] + str(self.user_score[0])
                                                   + " " * space_number[1] + str(self.user_score[1])), 1, (0, 0, 0))
            self.__win.blit(your_score, (115, 260))
            self.draw_scores(115, 290, item_number_11, top_eleven)

            # Draw button for restarting game
            try_again_logo = self.__big_text_font.render("Try again?", 1, (0, 0, 0))
            self.__win.blit(try_again_logo, (self.__width * (3 / 4) - try_again_logo.get_width() / 2,
                                             self.__height / 2 - try_again_logo.get_height() / 2 - 50))
            self.__win.blit(start_btn, (self.__btn[0] + self.__width / 4, self.__btn[1]))

            notification = self.__text_font.render("Visit our website: http://localhost:8000/", 1, (0, 0, 0))
            self.__win.blit(notification, (self.notification_position, 660))
            self.notification_position += 1
            if self.notification_position >= 1265:
                self.notification_position = -notification.get_width()

        pygame.display.update()

    def draw_scores(self, start_x, start_y, item_count, top_db_rows):

        best_score = self.__score_font.render(("Nickname:" + "      " + "Wave:" + "   " + "Enemy kill:"), 1, (0, 0, 0))
        self.__win.blit(best_score, (start_x, start_y))

        for row in range(item_count):
            space_number = (17 - len(top_db_rows[row][0]), 10 - len(top_db_rows[row][1]))
            best_score = self.__score_font.render((top_db_rows[row][0] + " " * space_number[0] + top_db_rows[row][1]
                                                   + " " * space_number[1] + top_db_rows[row][2]), 1, (0, 0, 0))
            self.__win.blit(best_score, (start_x, start_y + 30 * (row + 1)))

    @staticmethod
    def restart_game(game):
        game.clear_settings()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
