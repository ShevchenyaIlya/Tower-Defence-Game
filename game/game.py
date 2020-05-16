import pygame
import os
import string
import time
import random
import math

from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from enemies.troll import Troll
from enemies.sword import Sword
from enemies.goblin import Goblin
from towers.archer_tower import ArcherTowerLong, ArcherTowerShort
from towers.support_tower import RangeTower, DamageTower
from traps.traps import KillTrap, StopTrap, DestroyTrap
from menu.menu import VerticalMenu, PlayPauseButton
from game.image_collection import ControlImageCollection, ImageCollection
from game.level_settings import waves, bonus_wave, challenge_waves
from game.singleton import Singleton
from map.game_map import Map
from game.path_settings import Path

pygame.font.init()
pygame.mixer.pre_init(22050, -16, 2, 64)
pygame.mixer.init()
# pygame.init()

lives_img = ControlImageCollection("../game_assets/heart2.png", 36, 36).download_image()
star_img = ControlImageCollection("../game_assets/star1.png", 36, 36).download_image()
side_img = pygame.transform.rotate(ControlImageCollection("../game_assets/vertical_menu_1.png", 600, 125).download_image(), -90)
enemy_head = ControlImageCollection("../game_assets/head.png", 24, 24).download_image()
chit_code_table = ControlImageCollection("../game_assets/vertical_menu_1.png", 300, 60).download_image()

play_btn = ControlImageCollection("../game_assets/play_button_1.png", 75, 75).download_image()
pause_btn = ControlImageCollection("../game_assets/pause_button.png", 75, 75).download_image()
wave_bg = ControlImageCollection("../game_assets/wave.png", 200, 75).download_image()
username_bg = ControlImageCollection("../game_assets/wave.png", 300, 50).download_image()
small_star = ControlImageCollection("../game_assets/star1.png", 36, 36).download_image()

sound_btn = ControlImageCollection("../game_assets/music_icon.png", 75, 75).download_image()
sound_btn_off = ControlImageCollection("../game_assets/no_music_icon.png", 75, 75).download_image()

kill_trap_img = ControlImageCollection("../game_assets/traps_icon_3.png", 90, 90).download_image()
stop_trap_img = ControlImageCollection("../game_assets/traps_icon_1.png", 90, 90).download_image()
destroying_trap_img = ControlImageCollection("../game_assets/traps_icon_2.png", 90, 90).download_image()

tower_icon_img = ImageCollection("../game_assets/towers/tower image/", 4, 1, 64, 0, "tower_icon_")
tower_icon_img.download_tower()

attack_tower_names = ["archer_long", "archer_short"]
support_tower_names = ["range", "damage"]

points = []


@Singleton
class Game:
    path = []

    def __init__(self, win, username):
        self.__width = 1250
        self.__height = 700
        self.win = win
        self.enemies = []
        self.attack_towers = []
        self.support_towers = []
        self.traps = []
        self.__lives = 10
        self.__money = 200000
        self.__enemy_kill = 0
        self.bg = pygame.image.load(os.path.join("../game_assets/background_3.png")).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        self.game_map = None
        self.__timer = time.time()
        self.life_font = pygame.font.SysFont("life count", 30)
        self.username_font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        self.selected_tower = None
        self.object_orientation = []
        self.moving_object = None
        self.moving_effect = None
        self.wave = 15
        self.__current_wave = waves[self.wave][:]
        self.pause = True
        self.music_on = True
        self.username = username
        self.play_pause_button = PlayPauseButton(play_btn.convert_alpha(),
                                                 pause_btn.convert_alpha(),
                                                 10, self.__height - 85)
        self.sound_button = PlayPauseButton(sound_btn.convert_alpha(),
                                            sound_btn_off.convert_alpha(),
                                            90, self.__height - 85)

        self.stop_trap_btn = PlayPauseButton(stop_trap_img.convert_alpha(),
                                             stop_trap_img.convert_alpha(),
                                             1000, self.__height - 90)
        self.destroy_trap_btn = PlayPauseButton(destroying_trap_img.convert_alpha(),
                                                destroying_trap_img.convert_alpha(),
                                                915, self.__height - 90)

        self.menu = VerticalMenu(self.__width - side_img.get_width() + 80, 190, side_img)
        self.menu.add_btn(tower_icon_img.images[3].convert_alpha(), "buy_archer_1", 500)
        self.menu.add_btn(tower_icon_img.images[0].convert_alpha(), "buy_archer_2", 750)
        self.menu.add_btn(tower_icon_img.images[2].convert_alpha(), "buy_damage", 1000)
        self.menu.add_btn(tower_icon_img.images[1].convert_alpha(), "buy_range", 1000)

        self.is_input_chit = False
        self.current_chit_code = ""

    def game_map(self):
        return self.game_map

    def set_game_map(self, value):
        self.game_map = value
        if self.game_map == Map.FIRST_MAP:
            self.bg = pygame.image.load(os.path.join("../game_assets/background_1.png")).convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        elif self.game_map == Map.SECOND_MAP:
            self.bg = pygame.image.load(os.path.join("../game_assets/background_3.png")).convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        elif self.game_map == Map.THIRD_MAP:
            self.bg = pygame.image.load(os.path.join("../game_assets/background_2.png")).convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))
        elif self.game_map == Map.FOURTH_MAP:
            self.bg = pygame.image.load(os.path.join("../game_assets/background_4.png")).convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (self.__width, self.__height))

        Game.path = Path.get_path(self.game_map)

    @property
    def enemy_kill(self):
        return self.__enemy_kill

    @enemy_kill.setter
    def enemy_kill(self, value):
        self.__enemy_kill = value

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, value):
        self.__lives = value

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        self.__money = value

    def generate_enemies(self):
        """
        Generate the next enemy or enemies
        :return: enemy
        """
        if sum(self.__current_wave) == 0:
            if len(self.enemies) == 0:
                if self.wave == 10 and self.__money > 2000 and self.__enemy_kill > 100:
                    self.__current_wave = bonus_wave
                elif (self.wave + 1) % 5 == 0 and self.__lives == 10:
                    self.__current_wave = challenge_waves[self.wave // 5]
                else:
                    self.wave += 1
                    self.__current_wave = waves[self.wave]
                self.pause = True
                self.play_pause_button.pause = self.pause
        else:
            wave_enemies = [Scorpion(Game.path, self.game_map), Wizard(Game.path, self.game_map),
                            Club(Game.path, self.game_map), Troll(Game.path, self.game_map),
                            Sword(Game.path, self.game_map), Goblin(Game.path, self.game_map)]

            for x in range(len(self.__current_wave)):
                if self.__current_wave[x] != 0:
                    self.enemies.append(wave_enemies[x])
                    self.__current_wave[x] = self.__current_wave[x] - 1
                    break

    def run(self):
        # load music
        if self.game_map == Map.FIRST_MAP:
            pygame.mixer.music.load(os.path.join("../game_assets", "bensound-funnysong.wav"))
        elif self.game_map == Map.SECOND_MAP:
            pygame.mixer.music.load(os.path.join("../game_assets", "Fender_Bender.mp3"))
        elif self.game_map == Map.THIRD_MAP:
            pygame.mixer.music.load(os.path.join("../game_assets", "Shibuya.mp3"))
        elif self.game_map == Map.FOURTH_MAP:
            pygame.mixer.music.load(os.path.join("../game_assets", "Snow_Princess.mp3"))

        pygame.mixer.music.play(loops=-1)
        run = True

        clock = pygame.time.Clock()
        while run:
            clock.tick(100)

            if not self.pause:
                # generate monsters
                if time.time() - self.__timer >= random.randrange(1, 5) / 3:  # change speed of spanning enemies
                    self.__timer = time.time()
                    try:
                        self.generate_enemies()
                    except IndexError:
                        return True

            pos = pygame.mouse.get_pos()

            # check for moving effect
            if self.moving_effect:
                self.moving_effect.move(pos[0], pos[1])
                if self.point_to_line():
                    self.moving_effect.place_color = (255, 0, 0, 100)
                else:
                    self.moving_effect.place_color = (0, 255, 0, 100)

            # check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                if not self.point_to_line():
                    collide = True
                    self.moving_object.place_color = (255, 0, 0, 100)
                else:
                    if not collide:
                        self.moving_object.place_color = (0, 255, 0, 100)

                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 255, 0, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 255, 0, 100)

            # main events loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # get pressed key
                if event.type == pygame.KEYDOWN:

                    if event.key == 96:  # ~
                        if self.is_input_chit:
                            self.is_input_chit = False
                            self.current_chit_code = ""
                        else:
                            self.is_input_chit = True

                    if event.key == 13:  # Enter
                        self.is_input_chit = False
                        if self.current_chit_code == "money":
                            self.__money += 1000
                        elif self.current_chit_code == "lives":
                            self.__lives += 5
                        elif self.current_chit_code == "killall":
                            for enemy in self.enemies:
                                enemy.to_dying()

                        self.current_chit_code = ""

                    if self.is_input_chit:
                        pressed_keys = event.dict['unicode']

                        if event.key == pygame.K_BACKSPACE:
                            self.current_chit_code = self.current_chit_code[:-1]

                        if pressed_keys in string.ascii_letters or pressed_keys in string.digits:
                            if len(self.current_chit_code) <= 17:
                                self.current_chit_code += pressed_keys

                    """if event.key == 96:  # ~
                        self.key_phrase_input = True
                        self.pause = True
                        self.moving_effect = None

                    if event.key == 13:
                        if len(self.__key_phrase) == len(self.input_key_phrase) and self.__key_phrase == self.input_key_phrase:
                            self.__money += 1000
                        self.key_phrase_input = False
                        self.input_key_phrase.clear()

                    if self.key_phrase_input and event.key != 96:
                        self.input_key_phrase.append(event.key)"""

                if event.type == pygame.MOUSEBUTTONUP:
                    points.append(pos)
                    print(points)
                    if self.moving_effect:
                        if event.button == 3:
                            self.moving_effect = None
                        else:
                            destroy = False
                            if not self.point_to_line():
                                self.traps.append(self.moving_effect)
                                self.__money -= self.moving_effect.cost
                                destroy = True

                            if destroy:
                                self.moving_effect = None

                    # if your moving an object and click
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:] + self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True

                        # check if you try to place something on vertical menu surface
                        is_behind_menu = all(
                            [1110 < pos[0] < 1250, 120 < pos[1] < 670])

                        if is_behind_menu:
                            not_allowed = True

                        not_place_tower = False
                        if not not_allowed and self.point_to_line():
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)

                            not_place_tower = True

                        # delete moving object if you click right mouse button
                        if event.button == 3:  # right mouse click
                            if self.attack_towers and self.attack_towers[-1] is self.moving_object:
                                self.__money += self.moving_object.price
                                self.attack_towers = self.attack_towers[:-1]
                            elif self.support_towers and self.support_towers[-1] is self.moving_object:
                                self.__money += self.moving_object.price
                                self.support_towers = self.support_towers[:-1]

                        if not_place_tower:
                            self.moving_object.moving = False
                            self.moving_object = None

                    else:

                        if self.stop_trap_btn.click(pos[0], pos[1]):
                            if self.__money >= 150:
                                self.add_trap("stop_trap")
                        elif self.destroy_trap_btn.click(pos[0], pos[1]):
                            if self.__money >= 200:
                                self.add_trap("destroy_trap")

                        # check for play or pause
                        if self.play_pause_button.click(pos[0], pos[1]):
                            self.pause = not self.pause
                            ArcherTowerLong.is_game_pause = self.pause
                            self.play_pause_button.pause = self.pause

                        if self.sound_button.click(pos[0], pos[1]):
                            self.music_on = not self.music_on
                            self.sound_button.pause = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()

                        # look is you click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.__money >= cost:
                                self.__money -= cost
                                self.add_tower(side_menu_button)

                        # look is you click on attack tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if isinstance(cost, int) and self.__money >= cost:
                                        self.__money -= cost
                                        self.selected_tower.upgrade()

                        if not btn_clicked:
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

                            # look is you click on support tower
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

            if not self.pause:
                # loop through traps
                for trap in self.traps:
                    trap.stop_enemy(self.enemies)

                for trap in self.traps:
                    if trap.is_destroyed:
                        trap.destroy(self.traps, self.enemies)

                # loop through enemies
                to_del = []
                for en in self.enemies:
                    if en.is_die:
                        if en.animate_die(self.enemies):
                            self.__enemy_kill += 1
                    elif en.is_stopped_by_trap:
                        en.animate_attack()
                        en.stop_by_trap.is_attacked = True
                    else:
                        en.move()
                        if self.game_map == Map.SECOND_MAP or self.game_map == Map.THIRD_MAP:
                            if en.y > 715:
                                to_del.append(en)
                        elif self.game_map == Map.FIRST_MAP:
                            if en.x < -15:
                                to_del.append(en)
                        elif self.game_map == Map.FOURTH_MAP:
                            if en.x > 1265:
                                to_del.append(en)

                for enemy in self.enemies:
                    enemy.attack(self.traps)

                # delete all enemies off the screen
                for d in to_del:
                    self.__lives -= 1
                    self.enemies.remove(d)

                # if you lose
                if self.__lives <= 0:
                    print("You lose")
                    run = False

                # loop through attack towers
                for tw in self.attack_towers:
                    self.__money += tw.attack(self.enemies)

                # loop through support towers
                for tw in self.support_towers:
                    tw.support(self.attack_towers)

            self.draw()
        if self.__lives <= 0:
            return False
        pygame.quit()

    @staticmethod
    def point_to_line():
        """
        Returns if you can place tower based on distance from path
        :return: Bool
        """
        # find two closest points
        tower_x, tower_y = pygame.mouse.get_pos()
        first_closest_point = Game.path[0]

        for position, point in enumerate(Game.path[1:]):
            dis = math.sqrt((point[0] - tower_x) ** 2 + (point[1] - tower_y) ** 2)
            if math.sqrt((first_closest_point[0] - tower_x) ** 2 + (first_closest_point[1] - tower_y) ** 2) > dis:
                first_closest_point = (point[0], point[1], position)

        if (first_closest_point[0], first_closest_point[1]) != Game.path[0]:
            prev_point, next_point = Game.path[first_closest_point[2] - 1], Game.path[first_closest_point[2] + 1]
            first_distance = math.sqrt((prev_point[0] - tower_x) ** 2 + (prev_point[1] - tower_y) ** 2)
            second_distance = math.sqrt((next_point[0] - tower_x) ** 2 + (next_point[1] - tower_y) ** 2)
            if first_distance > second_distance:
                second_closest_point = prev_point
            else:
                second_closest_point = next_point
        else:
            second_closest_point = Game.path[1]

        # |ax + by + c|/(sqrt(a^2 + b^2))
        a = second_closest_point[1] - first_closest_point[1]
        b = - (second_closest_point[0] - first_closest_point[0])
        c = second_closest_point[0] * first_closest_point[1] - second_closest_point[1] * first_closest_point[0]
        denominator = math.sqrt(a ** 2 + b ** 2)

        distance = abs(a * tower_x + b * tower_y + c) / denominator
        if distance < 60:
            return False
        return True

    def draw(self):
        # draw background
        self.win.blit(self.bg, (0, 0))

        for point in points:
            pygame.draw.circle(self.win, (255, 0, 0), point, 3)

        # draw placement rings
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)
            for tower in self.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # redraw moving trap
        if self.moving_effect:
            self.moving_effect.draw_placement(self.win)

        # sort such objects for y coordinate and draw them in such sequence
        object_list = self.attack_towers[:] + self.support_towers[:] + self.enemies[:] + self.traps[:]
        object_list.sort(key=lambda x: x.y, reverse=False)
        for element in object_list:
            element.draw(self.win)

        """# loop through traps and draw health bar
        for trap in self.traps:
            if trap.is_attacked:
                trap.draw_health_bar(self.win)
                
        # loop through enemies and draw health bar
        for enemy in self.enemies:
            enemy.draw_health_bar(self.win)"""

        """# draw attack towers
        for tw in self.attack_towers:
            tw.draw(self.win)

        # draw support towers
        for tw in self.support_towers:
            tw.draw(self.win)

        # draw enemies
        for en in self.enemies:
            en.draw(self.win)"""

        # draw vertical menu
        self.menu.draw(self.win)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw_placement(self.win)
            self.moving_object.draw(self.win)

        # draw moving effect
        if self.moving_effect:
            self.moving_effect.draw_placement(self.win)
            self.moving_effect.draw(self.win)

        # draw play/pause button
        self.play_pause_button.draw(self.win)

        # draw traps buttons
        self.stop_trap_btn.draw(self.win)
        text = self.stop_trap_btn.font.render("150", 1, (255, 255, 255))
        self.win.blit(text, (self.stop_trap_btn.x + 35, self.stop_trap_btn.y + self.stop_trap_btn.height // 2 + 25))

        # self.kill_trap_btn.draw(self.win)
        self.destroy_trap_btn.draw(self.win)
        text = self.destroy_trap_btn.font.render("200", 1, (255, 255, 255))
        self.win.blit(text, (self.destroy_trap_btn.x + 35, self.destroy_trap_btn.y + self.destroy_trap_btn.height // 2 + 25))

        # draw music toggle button
        self.sound_button.draw(self.win)

        if self.game_map == Map.FOURTH_MAP:
            statistic_color = (0, 0, 0)
        else:
            statistic_color = (255, 255, 255)

        # draw lives
        text = self.life_font.render(str(self.__lives), 1, statistic_color)
        life = lives_img
        start_x = self.__width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width(), 20))
        self.win.blit(life, (start_x, 8))

        # draw username
        username = self.username_font.render(self.username, 1, (255, 255, 255))
        username_bg_transformed = pygame.transform.scale(username_bg, (username.get_width() + 100, username.get_height() + 25))
        start_x = self.__width - life.get_width() - text.get_width() - 30
        self.win.blit(username_bg_transformed, (start_x - username_bg_transformed.get_width(), 5))
        self.win.blit(username, (start_x - username_bg_transformed.get_width() + 55, 23))

        # draw currency
        text = self.life_font.render(str(self.__money), 1, statistic_color)
        start_x = self.__width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width(), 55))
        self.win.blit(star_img, (start_x, 40))

        # draw kills
        number_of_kills = self.life_font.render(str(self.__enemy_kill), 1, statistic_color)
        start_x = self.__width - life.get_width() - 10

        self.win.blit(number_of_kills, (start_x - number_of_kills.get_width(), 85))
        self.win.blit(enemy_head, (start_x + 8, 80))

        # draw wave
        self.win.blit(wave_bg, (10, 10))
        text = self.life_font.render("Wave #" + str(self.wave), 1, (255, 255, 255))
        self.win.blit(text, (10 + wave_bg.get_width() / 2 - text.get_width() / 2, 40))

        # draw chit code input table
        if self.is_input_chit:
            self.win.blit(chit_code_table, (self.__width // 2 - 150, self.__height - 60))

        if self.is_input_chit and self.current_chit_code:
            output_chit_string = self.life_font.render(self.current_chit_code, 1, (0, 0, 0))
            self.win.blit(output_chit_string, (self.__width // 2 - 100, self.__height - 40))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_archer_1", "buy_archer_2", "buy_damage", "buy_range"]
        object_list = [ArcherTowerLong(x, y), ArcherTowerShort(x, y), DamageTower(x, y), RangeTower(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

    def add_trap(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["stop_trap", "kill_trap", "destroy_trap"]
        object_list = [StopTrap(x, y), KillTrap(x, y), DestroyTrap(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_effect = obj
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

    def get_score(self):
        return self.wave, self.enemy_kill

    def clear_settings(self):
        self.__money = 2000
        self.__lives = 10
        self.wave = 0
        self.enemies.clear()
        self.attack_towers.clear()
        self.support_towers.clear()
        self.traps.clear()
        self.__enemy_kill = 0
        self.__timer = time.time()
        self.selected_tower = None
        self.object_orientation.clear()
        self.moving_object = None
        self.moving_effect = None
        self.__current_wave = waves[0][:]
        self.pause = True
        self.music_on = True
        self.is_input_chit = False
        self.current_chit_code = ""
        self.play_pause_button.pause = True
        self.sound_button.pause = True


if __name__ == "__main__":
    win = pygame.display.set_mode((1250, 700))
    g = Game(win)
    g.run()
