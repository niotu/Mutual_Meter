import pygame

from pygame import mixer
from lib.display import Display
from lib.clock import Clock
from lib.Car import Car
from lib.draw import draw_bg, draw_text, draw_health_bar
from lib.road import Road
from lib.Menu import MainMenu


# метод для проигрывания музыки
def play_music_bg(music_bg):
    mixer.stop()
    mixer.music.load(music_bg)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)


def restart_round():
    global player, road
    player = Car(display, CAR_DATA, car_sheet, CAR_ANIMATION_STEPS)
    road = Road(display, player)


def drive(car):
    global score, highest_score, game_on, score_speed
    draw_bg(bg_road)

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
car_sheet = pygame.image.load(r"assets\images\sprites\car_sprite_sheet.png").convert_alpha()

# шрифт
font = pygame.font.SysFont('Times New Roman', 40)

# параметры картинки
CAR_SIZE = 650
CAR_SCALE = 1 * display.scr_w
CAR_OFFSET = [227, 168]
CAR_DATA = [CAR_SIZE, CAR_SCALE, CAR_OFFSET]
CAR_ANIMATION_STEPS = [3, 3]

# Загрузка классов
player = Car(display, CAR_DATA, car_sheet, CAR_ANIMATION_STEPS)
road = Road(display, player)
game_menu = MainMenu(display.scr_w, display.scr_h, bg_road, font)

game_on = False
score = 0
score_speed = 1
highest_score = 0

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
    if game_on:
        drive(player)
    pygame.display.flip()

    # Обновление кадра дисплея
    pygame.display.update()

pygame.quit()
