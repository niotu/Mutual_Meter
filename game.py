import pygame
from pygame import mixer

from const.CONSTANTS import *
from lib.Car import Car
from lib.Menu import MainMenu, ShopMenu, Button, UpgradesMenu
from lib.clock import Clock
from lib.display import Display
# from lib.draw import draw_bg, draw_text, draw_health_bar
from lib.road import Road
from lib.storage import Storage


class Game:
    def __init__(self):

        # Загрузка дисплея с его прилежащими методами
        self.display = Display()

        # Загрузка клока
        self.clocks = Clock()
        self.storage = Storage()

        # Загрузка картинок
        self.bg_road = pygame.image.load(r"assets\images\backgrounds\road.png").convert_alpha()
        self.logo = pygame.image.load(r"assets\images\mutual_meter.png").convert_alpha()
        self.red_car_sheet = pygame.image.load(TAGS_TO_LINKS['red_car']).convert_alpha()
        self.police_car_sheet = pygame.image.load(TAGS_TO_LINKS['police_car']).convert_alpha()
        self.grey_car_sheet = pygame.image.load(
            r"assets\images\pixel_sprites\car_grey_sprite_sheet.png").convert_alpha()
        self.rock_sheet = pygame.image.load(r"assets\images\pixel_sprites\rock_sprite_sheet.png").convert_alpha()
        self.sign_sheet = pygame.image.load(r"assets\images\pixel_sprites\sign_sprite_sheet.png").convert_alpha()
        self.obstacles_sheets = [self.grey_car_sheet, self.sign_sheet, self.rock_sheet]
        self.health_sheet = pygame.image.load(r"assets\images\pixel_sprites\boosters\heal_sheet.png").convert_alpha()
        self.shield_sheet = pygame.image.load(r"assets\images\pixel_sprites\boosters\shield_sheet.png").convert_alpha()
        self.boosters_sheets = [self.health_sheet, self.shield_sheet]
        self.shield_sprite = pygame.image.load(r"assets\images\pixel_sprites\boosters\shield.png").convert_alpha()
        self.heart_sprite = pygame.image.load(r"assets\images\pixel_sprites\boosters\heart.png").convert_alpha()
        # шрифт
        self.font = pygame.font.Font(r'assets\fonts\press-start\prstart.ttf', 40)
        self.small_font = pygame.font.Font(r'assets\fonts\press-start\prstart.ttf', 20)

        self.application_run = True
        self.game_on = False
        self.score_speed = 1

        self.levels_upgrade = self.storage.get_upgrades_levels()
        self.shield_speed, self.max_health = self.storage.get_upgrades_params()

        self.state = 0
        self.score = 0
        self.level_score = 0
        self.current_skin_index = self.storage.get_current_car_index()
        self.cars = ['red_car',
                     'green_car',
                     'brown_car',
                     'police_car']

        self.highest_score, self.money = self.load_scores()
        self.bought_cars = self.storage.get_bought_cars()
        # self.current_car = self.storage.get_current_car()

        # Загрузка классов
        self.player = Car(self.display, CAR_DATA, self.cars[self.current_skin_index], True, self.max_health)
        # self.player = Car(self.display, CAR_DATA, self.storage.get_current_car())
        self.road = Road(self.display, self.player, (self.obstacles_sheets, self.boosters_sheets), [CAR_DATA, CAR_DATA])
        self.game_menu = MainMenu(self.display.scr_w, self.display.scr_h, self.bg_road, self.font, self.logo)
        self.shop_menu = ShopMenu(self.display.scr_w, self.display.scr_h, self.bg_road, self.font, self.bought_cars,
                                  self.player)
        self.upgrades_menu = UpgradesMenu(self.display.scr_w, self.display.scr_h, self.bg_road, self.font)
        self.exit_button = Button('Exit', self.font, (300, 100), (1500, 100))

    # метод для проигрывания музыки
    def play_music_bg(self, music_bg):
        mixer.stop()
        mixer.music.load(music_bg)
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

    def restart_round(self):
        # sheet = self.player.sprite_sheet
        if self.highest_score < self.score // 10:
            self.highest_score = self.score // 10
        self.money += self.score // 100
        self.score = 0
        self.score_speed = 1
        self.player.revive()
        self.road = Road(self.display, self.player, (self.obstacles_sheets, self.boosters_sheets),
                         [CAR_DATA, CAR_DATA, CAR_DATA])


    def drive(self, car, mouse_click):
        self.display.draw_bg(self.bg_road)
        self.exit_button.show()
        self.exit_button.click(mouse_click)
        self.display.draw_text(f"$: {(self.score // 100) + self.money}", self.font, (255, 255, 255), 50 * SCREEN_WIDTH,
                               150 * SCREEN_HEIGHT)
        self.display.draw_text(f"SCORE: {self.score // 10}", self.font, (255, 255, 255), 50 * SCREEN_WIDTH,
                               200 * SCREEN_HEIGHT)
        if self.score // 10 <= self.highest_score:
            self.display.draw_text(f"HIGHEST IN: {self.highest_score - self.score // 10}", self.small_font,
                                   (255, 255, 255),
                                   50 * SCREEN_WIDTH,
                                   250 * SCREEN_HEIGHT)
        self.display.draw_text(f"LEVEL {self.road.get_level()}", self.font,
                               (255, 255, 255),
                               50 * SCREEN_WIDTH,
                               300 * SCREEN_HEIGHT)
        if self.player.alive:
            self.score += self.score_speed
            self.level_score += 1
            if self.score % 500 == 0:
                self.road.speed += 1
                self.score_speed += 1
        elif not self.player.alive:
            self.game_on = False
            self.game_menu.enable()
            self.restart_round()

        # draw player
        self.road.generate(self.level_score)
        self.player.move(self.shield_speed)
        self.player.update()
        self.player.draw(self.display.screen)
        # show players stats
        if car.hit_cooldown > 0:
            self.display.draw_hit_cooldown(car.hit_cooldown * 2, self.shield_sprite)
        self.display.draw_health_bar(car.health, 65 * SCREEN_WIDTH, 20 * SCREEN_HEIGHT, self.heart_sprite, self.max_health)

    def game_navigation(self, mouse_click):
        if self.game_menu.is_enabled():
            self.game_menu.show(mouse_click)
            self.display.draw_text(f"HIGHEST SCORE: {self.highest_score}", self.font, (255, 255, 255),
                                   650 * SCREEN_WIDTH,
                                   520 * SCREEN_HEIGHT)
            if self.game_menu.exit_button.is_clicked():
                self.application_run = False
            if self.game_menu.start_button.is_clicked():
                self.game_menu.disable()
                self.game_on = True
            if self.game_menu.shop_button.is_clicked():
                self.shop_menu.enable()
                self.game_menu.disable()
            if self.game_menu.upgrades_button.is_clicked():
                self.upgrades_menu.enable()
                self.game_menu.disable()
        if self.shop_menu.is_enabled():
            '''enter the shop'''
            # game.load_shop(game.player)
            self.shop_menu.show(mouse_click)
            if self.shop_menu.back_button.is_clicked():
                self.shop_menu.disable()
                self.game_menu.enable()
            if self.shop_menu.next_car.is_clicked():
                self.current_skin_index = (self.current_skin_index + 1) % len(self.cars)
                self.player.change_skin(self.cars[self.current_skin_index])
                self.shop_menu.next_car.clicked = False
            if self.shop_menu.prev_car.is_clicked():
                self.current_skin_index = (self.current_skin_index - 1) % len(self.cars)
                self.player.change_skin(self.cars[self.current_skin_index])
                self.shop_menu.prev_car.clicked = False

        if self.upgrades_menu.is_enabled():
            self.upgrades_menu.show(mouse_click, self.levels_upgrade, self.money)
            self.display.draw_text(f"{self.money}$", self.font, (255, 255, 255), 810 * self.display.scr_w,
                                   300 * self.display.scr_h)
            self.display.draw_image(self.shield_sprite, (200, 200), (20, 650))
            self.display.draw_image(self.heart_sprite, (200, 200), (650, 650))
            if self.upgrades_menu.back_button.is_clicked():
                self.game_menu.enable()
                self.upgrades_menu.disable()
            if self.upgrades_menu.upgrade_shield_button.is_clicked():
                self.levels_upgrade[0] += 1
                self.shield_speed -= 0.05
                self.money -= self.upgrades_menu.costs[0]
            if self.upgrades_menu.upgrade_health_button.is_clicked():
                self.levels_upgrade[1] += 1
                self.max_health += 10
                self.player.health = self.max_health
                self.player.max_health = self.max_health
                self.money -= self.upgrades_menu.costs[1]

        if self.game_on:
            if self.exit_button.is_clicked():
                self.game_on = False
                self.game_menu.enable()
                self.restart_round()
            if self.highest_score < self.score // 10:
                self.highest_score = self.score // 10
            self.drive(self.player, mouse_click)

    def update_skins(self):
        self.player.update()
        self.road.update_obstacles()
        self.game_menu.update_animation()

    def load_scores(self):
        stor = self.storage.get_storage()
        highest_score = stor.get('highest_score')
        money = stor.get('money')
        return int(highest_score), int(money)

    def quit(self):
        self.storage.save_data(self.highest_score, self.money, self.levels_upgrade,
                               [self.shield_speed, self.max_health])
