import json

import pygame
from lib.video_reader import VideoReader
from lib.display import Display
from lib.mixer import button_sound

display = Display()
bar = VideoReader(r"assets\video\bar2.mp4")


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, font, size, pos):
        self.x, self.y = pos
        self.size = self.width, self.height = size
        self.font = font
        self.text = text
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.change_text(text)
        # self.bought = False
        self.render = None
        self.color = "white"

    def change_text(self, text, bg="white"):
        self.render = self.font.render(text, 1, pygame.Color("Black"))
        self.surface.fill(bg)
        self.surface.blit(self.render, (self.width // 2 - 70, self.height // 2 - 30))

    def show(self):
        self.clicked = False
        display.screen.blit(self.surface, (self.x, self.y))
        self.change_text(self.text, self.color)
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def click(self, mouse_click):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.color = "red"
            if mouse_click:
                self.clicked = True
                pygame.mixer.Sound.play(button_sound)
        else:
            self.color = "white"

    def is_clicked(self):
        return self.clicked


class MainMenu:
    def __init__(self, scr_w, scr_h, bg, font, logo):
        self.start_button = Button("START", font,
                                   (400 * scr_w, 200 * scr_h),
                                   (1200 * scr_w, 800 * scr_h))
        self.exit_button = Button("EXIT", font,
                                  (400 * scr_w, 200 * scr_h),
                                  (400 * scr_w, 800 * scr_h))
        self.shop_button = Button("CARS", font,
                                  (400 * scr_w, 100 * scr_h),
                                  (1470 * scr_w, 50 * scr_h))
        self.upgrades_button = Button("SHOP", font,
                                      (400 * scr_w, 100 * scr_h),
                                      (30 * scr_w, 50 * scr_h))
        self.logo = logo
        self.bg = bg
        self.enabled = True

    def show(self, mouse_click):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        scaled_logo = pygame.transform.scale(self.logo, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_logo, (0, 0))
        bar.draw_animated_bg()
        self.start_button.show()
        self.exit_button.show()
        self.shop_button.show()
        self.upgrades_button.show()
        self.exit_button.click(mouse_click)
        self.start_button.click(mouse_click)
        self.shop_button.click(mouse_click)
        self.upgrades_button.click(mouse_click)

    def update_animation(self):
        pass

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


class ShopMenu:
    def __init__(self, scr_w, scr_h, bg, font, price_list, curr_car):
        self.prev_car = Button("<--", font,
                               (400 * scr_w, 100 * scr_h),
                               (300 * scr_w, 400 * scr_h))
        self.next_car = Button("-->", font,
                               (400 * scr_w, 100 * scr_h),
                               (1200 * scr_w, 400 * scr_h))
        self.back_button = Button("BACK", font,
                                  (400 * scr_w, 100 * scr_h),
                                  (50 * scr_w, 50 * scr_h))

        self.price_list = self.load_price_list()
        self.shop_items = list(self.price_list.keys())
        self.current_car = curr_car
        self.bg = bg
        self.enabled = False

    def show(self, mouse_click):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        self.current_car.update()
        self.current_car.draw(display.screen)

        self.prev_car.show()
        self.next_car.show()
        self.back_button.show()

        self.back_button.click(mouse_click)
        self.next_car.click(mouse_click)
        self.prev_car.click(mouse_click)

    def change_shop_item(self, destination):
        pass

    def buy(self, money, car):
        price = int(self.price_list[car])
        if money >= price and not car.bought:
            car.buy()
            return money - price
        else:
            return money

    def load_price_list(self):
        with open('storage/prices.json', 'r') as f:
            price = json.load(f)
        return price

    def update_car(self):
        pass

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


class UpgradesMenu:
    def __init__(self, scr_w, scr_h, bg, font):
        self.back_button = Button("BACK", font,
                                  (400 * scr_w, 100 * scr_h),
                                  (750 * scr_w, 50 * scr_h))
        self.upgrade_shield_button = Button("MAX", font,
                                            (300 * scr_w, 100 * scr_h),
                                            (300 * scr_w, 700 * scr_h))
        self.upgrade_health_button = Button("MAX", font,
                                            (300 * scr_w, 100 * scr_h),
                                            (900 * scr_w, 700 * scr_h))
        self.upgrade_money_button = Button("MAX", font,
                                           (300 * scr_w, 100 * scr_h),
                                           (1480 * scr_w, 700 * scr_h))
        self.font = font
        self.bg = bg
        self.enabled = False
        self.costs = [200, 200, 200]

    def update_buttons(self):
        self.upgrade_shield_button.text = str(self.costs[0])
        self.upgrade_health_button.text = str(self.costs[1])
        self.upgrade_money_button.text = str(self.costs[2])

    def show(self, mouse_click, lvls, money):
        self.update_buttons()
        self.costs = [200 * lvls[0], 200 * lvls[1], 200 * lvls[2]]
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        display.draw_text(f"{round(money)}$", self.font, (255, 255, 255), 810 * display.scr_w,
                          300 * display.scr_h)
        display.draw_text(str(lvls[0]), self.font, (255, 255, 255), 400, 600)
        display.draw_text(str(lvls[1]), self.font, (255, 255, 255), 1000, 600)
        display.draw_text(str(lvls[2]), self.font, (255, 255, 255), 1580, 600)
        self.back_button.show()
        self.upgrade_shield_button.show()
        self.upgrade_health_button.show()
        self.upgrade_money_button.show()

        self.back_button.click(mouse_click)
        if lvls[0] > 9:
            self.upgrade_shield_button.change_text("MAX")
        elif money < self.costs[0]:
            self.upgrade_shield_button.change_text(self.upgrade_shield_button.text, "white")
        else:
            self.upgrade_shield_button.click(mouse_click)
        if lvls[1] > 9:
            self.upgrade_health_button.change_text("MAX")
        elif money < self.costs[1]:
            self.upgrade_health_button.change_text(self.upgrade_health_button.text, "white")
        else:
            self.upgrade_health_button.click(mouse_click)
        if lvls[2] > 9:
            self.upgrade_money_button.change_text("MAX")
        elif money < self.costs[2]:
            self.upgrade_money_button.change_text(self.upgrade_money_button.text, "white")

        else:
            self.upgrade_money_button.click(mouse_click)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
