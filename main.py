import pygame

from pygame import mixer
from lib.display import Display
from lib.clock import Clock
from lib.Car import Car
from lib.draw import draw_bg, draw_text, draw_health_bar
from lib.road import Road
from lib.Menu import MainMenu, ShopMenu


# метод для проигрывания музыки
def play_music_bg(music_bg):
    mixer.stop()
    mixer.music.load(music_bg)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)


def restart_round():
    global player, road
    player = Car(display, CAR_DATA, red_car_sheet, CAR_ANIMATION_STEPS)
    road = Road(display, player)


def drive(car):
    global score, highest_score, game_on, score_speed, money
    draw_bg(bg_road)
    draw_text(f"$: {(score // 100) + money}", font, (255, 255, 255), 50 * display.scr_w, 150 * display.scr_h)
    draw_text(f"SCORE: {score // 10}", font, (255, 255, 255), 50 * display.scr_w, 200 * display.scr_h)
    if score // 10 < highest_score:
        draw_text(f"HIGHEST IN: {highest_score - score // 10}", font, (255, 255, 255), 50 * display.scr_w, 250 * display.scr_h)
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
    player.draw(display.screen)


# Инициализация
pygame.init()
mixer.init()

# Загрузка дисплея с его прилежащими методами
display = Display()

# Загрузка клока
clocks = Clock()

# Загрузка картинок
bg_road = pygame.image.load(r"assets\images\backgrounds\road.png").convert_alpha()
red_car_sheet = pygame.image.load(r"assets\images\sprites\car_sprite_sheet.png").convert_alpha()
police_car_sheet = pygame.image.load(r"assets\images\sprites\car_police_sprite_sheet.png").convert_alpha()


# шрифт
font = pygame.font.SysFont('Times New Roman', 40)

# параметры картинки
CAR_SIZE = 650
CAR_SCALE = 1 * display.scr_w
CAR_OFFSET = [227, 168]
CAR_DATA = [CAR_SIZE, CAR_SCALE, CAR_OFFSET]
CAR_ANIMATION_STEPS = [3, 3]

# Загрузка классов
player = Car(display, CAR_DATA, red_car_sheet, CAR_ANIMATION_STEPS)
road = Road(display, player)
game_menu = MainMenu(display.scr_w, display.scr_h, bg_road, font)
shop_menu = ShopMenu(display.scr_w, display.scr_h, bg_road, font)

game_on = False
score = 0
score_speed = 1
highest_score = 0
money = 0

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
        draw_text(f"HIGHEST SCORE: {highest_score}", font, (255, 255, 255), 810 * display.scr_w, 300 * display.scr_h)
        if game_menu.exit_button.is_clicked():
            run = False
        if game_menu.start_button.is_clicked():
            game_menu.disable()
            game_on = True
        if game_menu.shop_button.is_clicked():
            shop_menu.enable()
            game_menu.disable()
    if shop_menu.is_enabled():
        shop_menu.show(money)
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

pygame.quit()
