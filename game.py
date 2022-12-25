import pygame
from pygame import mixer

from lib.Car import Car
from lib.Menu import MainMenu, ShopMenu
from lib.clock import Clock
from lib.display import Display
from lib.draw import draw_bg, draw_text, draw_health_bar
from lib.road import Road
from lib.storage import Storage
from const.CONSTANTS import *

class Game:
    def __init__(self):

        # Загрузка дисплея с его прилежащими методами
        self.display = Display()

        # Загрузка клока
        self.clocks = Clock()

        # Загрузка картинок
        self.bg_road = pygame.image.load(r"assets\images\backgrounds\road.png").convert_alpha()
        self.logo = pygame.image.load(r"assets\images\mutual_meter.png").convert_alpha()
        self.red_car_sheet = pygame.image.load(
            r"assets\images\pixel_sprites\car_sprites\car_sprite_sheet.png").convert_alpha()
        self.police_car_sheet = pygame.image.load(r"assets\images\pixel_sprites\car_police_sprite_sheet.png").convert_alpha()
        self.grey_car_sheet = pygame.image.load(r"assets\images\pixel_sprites\car_grey_sprite_sheet.png").convert_alpha()
        self.rock_sheet = pygame.image.load(r"assets\images\pixel_sprites\rock_sprite_sheet.png").convert_alpha()
        self.sign_sheet = pygame.image.load(r"assets\images\pixel_sprites\sign_sprite_sheet.png").convert_alpha()

        self.obstacles_sheets = [self.grey_car_sheet, self.sign_sheet, self.rock_sheet]
        # шрифт
        self.font = pygame.font.Font(r'assets\fonts\press-start\prstart.ttf', 40)
        self.small_font = pygame.font.Font(r'assets\fonts\press-start\prstart.ttf', 20)

        # Загрузка классов
        self.player = Car(self.display, CAR_DATA, self.red_car_sheet)
        self.road = Road(self.display, self.player, self.obstacles_sheets, [CAR_DATA, CAR_DATA])
        self.game_menu = MainMenu(self.display.scr_w, self.display.scr_h, self.bg_road, self.font, self.logo)
        self.shop_menu = ShopMenu(self.display.scr_w, self.display.scr_h, self.bg_road, self.font)
        self.storage = Storage()

        self.game_on = False
        self.score_speed = 1

        self.state = 0
        self.score = 0

        self.highest_score, self.money = self.load_scores()


    # метод для проигрывания музыки
    def play_music_bg(self, music_bg):
        mixer.stop()
        mixer.music.load(music_bg)
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)


    def restart_round(self):
        sheet = self.player.sprite_sheet
        self.player = Car(self.display, CAR_DATA, sheet)
        self.road = Road(self.display, self.player, self.obstacles_sheets, [CAR_DATA, CAR_DATA, CAR_DATA])


    def drive(self, car):
        self.display.draw_bg(self.bg_road)
        self.display.draw_text(f"$: {(self.score // 100) + self.money}", self.font, (255, 255, 255), 50 * SCREEN_WIDTH, 150 * SCREEN_HEIGHT)
        self.display.draw_text(f"SCORE: {self.score // 10}", self.font, (255, 255, 255), 50 * SCREEN_WIDTH, 200 * SCREEN_HEIGHT)
        if self.score // 10 <= self.highest_score:
            draw_text(f"HIGHEST IN: {self.highest_score - self.score // 10}", self.small_font, (255, 255, 255), 50 * SCREEN_WIDTH,
                      250 * SCREEN_HEIGHT)
        if self.player.alive:
            self.score += self.score_speed
            if self.score % 500 == 0:
                self.road.speed += 1
                self.score_speed += 1
        else:
            self.game_on = False
            self.game_menu.enable()
            self.restart_round()
            if self.highest_score < self.score // 10:
                self.highest_score = self.score // 10
            self.money += self.score // 100
            self.score = 0
            self.score_speed = 1
        # show players stats
        draw_health_bar(car.health, 20 * SCREEN_WIDTH, 20 * SCREEN_HEIGHT)
        # draw player
        self.road.generate()
        self.player.move()
        self.player.update()
        if self.player.hit_cooldown % 5 == 0:
            self.player.draw(self.display.screen)


    def load_scores(self):
        stor = self.storage.get_storage()
        highest_score = stor.get('highest_score')
        money = stor.get('money')
        return int(highest_score), int(money)

    def quit(self):
        bought_cars = []
        self.storage.save_data(self.highest_score, self.money, bought_cars)

