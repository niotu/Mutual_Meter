import pygame

from const.CONSTANTS import *
from game import Game

pygame.init()

game = Game()
# Луп игры
application_run = True
while application_run:
    game.clocks.clock.tick(FPS)

    # Хэндлер
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            application_run = False
    if game.game_menu.is_enabled():
        game.game_menu.show()
        game.display.draw_text(f"HIGHEST SCORE: {game.highest_score}", game.font, (255, 255, 255), 650 * SCREEN_WIDTH,
                               520 * SCREEN_HEIGHT)
        if game.game_menu.exit_button.is_clicked():
            application_run = False
        if game.game_menu.start_button.is_clicked():
            game.game_menu.disable()
            game.game_on = True
        if game.game_menu.shop_button.is_clicked():
            game.shop_menu.enable()
            game.game_menu.disable()
    if game.shop_menu.is_enabled():
        '''enter the shop'''
        # game.load_shop(game.player)
        game.shop_menu.show()
        game.display.draw_text(f"{game.money}$", game.font, (255, 255, 255), 810 * game.display.scr_w,
                               300 * game.display.scr_h)
        if game.shop_menu.back_button.is_clicked():
            game.shop_menu.disable()
            game.game_menu.enable()
        if game.shop_menu.next_car.is_clicked():
            game.current_skin_index = (game.current_skin_index + 1) % len(game.cars)
            game.player.change_skin(game.cars[game.current_skin_index])
            game.shop_menu.next_car.clicked = False
        if game.shop_menu.prev_car.is_clicked():
            game.current_skin_index = (game.current_skin_index - 1) % len(game.cars)
            game.player.change_skin(game.cars[game.current_skin_index])
            game.shop_menu.prev_car.clicked = False

            # if game.shop_menu.police_car.bought:
        #         game.player.change_skin(game.police_car_sheet)
        #     else:
        #         game.shop_menu.police_car.bought = True
        #         game.money -= 200
        #         game.player.change_skin(game.police_car_sheet)

    if game.game_on:
        game.drive(game.player)

    pygame.display.flip()

    # Обновление кадра дисплея
    pygame.display.update()

game.quit()
pygame.quit()
