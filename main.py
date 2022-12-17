import pygame

from pygame import mixer
from lib.display import Display
from lib.clock import Clock
from lib.Car import Car
from lib.road import Road
from lib.Menu import MainMenu


# метод для проигрывания музыки
def play_music_bg(music_bg):
    mixer.stop()
    mixer.music.load(music_bg)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)


# метод для написания текста
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    display.screen.blit(img, (x, y))


# function for drawing bg
def draw_bg(bg):
    scaled_bg = pygame.transform.scale(bg, (display.screen_width, display.screen_height))
    display.screen.blit(scaled_bg, (0, 0))


# function to draw health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(display.screen, (255, 255, 255), (x - 2, y - 2, 404 * display.scr_w, 34 * display.scr_h))
    pygame.draw.rect(display.screen, (255, 0, 0), (x, y, 400 * display.scr_w, 30 * display.scr_h))
    pygame.draw.rect(display.screen, (100, 0, 0), (x, y + 15, 400 * display.scr_w, 15 * display.scr_h))
    pygame.draw.rect(display.screen, (250, 200, 0), (x, y, 400 * ratio * display.scr_w, 30 * display.scr_h))
    pygame.draw.rect(display.screen, (195, 155, 0), (x, y + 20, 400 * ratio * display.scr_w, 10 * display.scr_h))
    pygame.draw.rect(display.screen, (255, 255, 0), (x, y, 400 * ratio * display.scr_w, 10 * display.scr_h))


def restart_round():
    global player, road
    player = Car(display)
    road = Road(display, player)


def drive(car):
    global score, game_on, highest_score
    draw_bg(bg_road)

    draw_text(f"SCORE: {score}", font, (255, 255, 255), 50 * display.scr_w, 200 * display.scr_h)
    if player.alive:
        score += 1
    else:
        game_on = False
        game_menu.enable()
        if highest_score < score:
            highest_score = score
            score = 0
            restart_round()
    # show players stats
    draw_health_bar(car.health, 20 * display.scr_w, 20 * display.scr_h)
    # draw player
    road.generate()
    player.move()
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

# шрифт
font = pygame.font.SysFont('Times New Roman', 40)

# Загрузка классов
player = Car(display)
road = Road(display, player)
game_menu = MainMenu(display.scr_w, display.scr_h, bg_road, font)

game_on = False
score = 0
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
