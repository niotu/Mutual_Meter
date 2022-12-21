import pygame

from pygame import mixer
from lib.display import Display
from lib.clock import Clock
from lib.Car import Car
from lib.draw import draw_bg, draw_text, draw_health_bar
from lib.road import Road
from lib.Menu import MainMenu, ShopMenu
from lib.storage import Storage


# метод для проигрывания музыки
def play_music_bg(music_bg):
    mixer.stop()
    mixer.music.load(music_bg)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)


def restart_round():
    global player, road
    sheet = player.sprite_sheet
    player = Car(display, CAR_DATA, sheet)
    road = Road(display, player, [grey_car_sheet, grey_car_sheet, sign_sheet], [CAR_DATA, CAR_DATA, CAR_DATA])


def drive(car):
    global score, highest_score, game_on, score_speed, money
    draw_bg(bg_road)
    draw_text(f"$: {(score // 100) + money}", font, (255, 255, 255), 50 * display.scr_w, 150 * display.scr_h)
    draw_text(f"SCORE: {score // 10}", font, (255, 255, 255), 50 * display.scr_w, 200 * display.scr_h)
    if score // 10 <= highest_score:
        draw_text(f"HIGHEST IN: {highest_score - score // 10}", small_font, (255, 255, 255), 50 * display.scr_w,
                  250 * display.scr_h)
    if player.alive:
        score += score_speed
        if score % 500 == 0:
            road.speed += 1
            score_speed += 1
    else:
        game_on = False
        game_menu.enable()
        restart_round()
        if highest_score < score // 10:
            highest_score = score // 10
        money += score // 100
        score = 0
        score_speed = 1
    # show players stats
    draw_health_bar(car.health, 20 * display.scr_w, 20 * display.scr_h)
    # draw player
    road.generate()
    player.move()
    player.update()
    if player.hit_cooldown % 5 == 0:
        player.draw(display.screen)

def set_scores():
    stor = storage.get_storage()
    highest_score = stor.get('highest_score')
    money = stor.get('money')
    return int(highest_score), int(money)

score = 0


# Инициализация
pygame.init()
mixer.init()

# Загрузка дисплея с его прилежащими методами
display = Display()

# Загрузка клока
clocks = Clock()

# Загрузка картинок
bg_road = pygame.image.load(r"assets\images\backgrounds\road.png").convert_alpha()
logo = pygame.image.load(r"assets\images\mutual_meter.png").convert_alpha()
red_car_sheet = pygame.image.load(r"assets\images\pixel_sprites\car_sprites\car_sprite_sheet.png").convert_alpha()
police_car_sheet = pygame.image.load(r"assets\images\pixel_sprites\car_police_sprite_sheet.png").convert_alpha()
grey_car_sheet = pygame.image.load(r"assets\images\pixel_sprites\car_grey_sprite_sheet.png").convert_alpha()

rock_sheet = pygame.image.load(r"assets\images\pixel_sprites\rock_sprite_sheet.png").convert_alpha()
sign_sheet = pygame.image.load(r"assets\images\pixel_sprites\sign_sprite_sheet.png").convert_alpha()

# шрифт
font = pygame.font.Font(r'assets\fonts\press-start\prstart.ttf', 40)
small_font = pygame.font.Font(r'assets\fonts\press-start\prstart.ttf', 20)

# параметры спрайтов
CAR_SIZE = 83
CAR_SCALE = 7.1 * display.scr_w
CAR_OFFSET = [29, 21]
CAR_DATA = [CAR_SIZE, CAR_SCALE, CAR_OFFSET, [3, 3]]

# Загрузка классов
player = Car(display, CAR_DATA, red_car_sheet)
road = Road(display, player, [grey_car_sheet, rock_sheet, sign_sheet], [CAR_DATA, CAR_DATA])
game_menu = MainMenu(display.scr_w, display.scr_h, bg_road, font, logo)
shop_menu = ShopMenu(display.scr_w, display.scr_h, bg_road, font)
storage = Storage()

game_on = False
score_speed = 1

highest_score, money = set_scores()

# Луп игры
run = True
while run:
    clocks.clock.tick(clocks.fps)

    # Хэндлер
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    if game_menu.is_enabled():
        game_menu.show()
        draw_text(f"HIGHEST SCORE: {highest_score}", font, (255, 255, 255), 650 * display.scr_w, 520 * display.scr_h)
        if game_menu.exit_button.is_clicked():
            run = False
        if game_menu.start_button.is_clicked():
            game_menu.disable()
            game_on = True
        if game_menu.shop_button.is_clicked():
            shop_menu.enable()
            game_menu.disable()
    if shop_menu.is_enabled():
        '''enter the shop'''
        shop_menu.show(money, player)
        draw_text(f"{money}$", font, (255, 255, 255), 810 * display.scr_w, 300 * display.scr_h)
        if shop_menu.back_button.is_clicked():
            shop_menu.disable()
            game_menu.enable()
        if shop_menu.red_car.is_clicked():
            player.change_skin(red_car_sheet)
        if shop_menu.police_car.is_clicked():
            if shop_menu.police_car.bought:
                player.change_skin(police_car_sheet)
            else:
                shop_menu.police_car.bought = True
                money -= 200
                player.change_skin(police_car_sheet)

    if game_on:
        drive(player)
    pygame.display.flip()

    # Обновление кадра дисплея
    pygame.display.update()

storage.save_data(highest_score, money, [])
pygame.quit()
