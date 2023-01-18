import pygame

from const.CONSTANTS import *
from game import Game

pygame.init()

game = Game()
# Луп игры
mouse_click = False
while game.application_run:
    game.clocks.clock.tick(FPS)

    # Хэндлер
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game.application_run = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = True
    game.game_navigation(mouse_click)

    mouse_click = False
    pygame.display.flip()

    # Обновление кадра дисплея
    pygame.display.update()

game.quit()
pygame.quit()
