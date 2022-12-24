import json

import pygame

from lib.display import Display

display = Display()


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

    def change_text(self, text, bg="white"):
        self.render = self.font.render(text, 1, pygame.Color("Black"))
        self.surface.fill(bg)
        self.surface.blit(self.render, (self.width // 2 - 70, self.height // 2 - 30))

    def show(self):
        self.clicked = False
        display.screen.blit(self.surface, (self.x, self.y))
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def click(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.change_text(self.text, "red")
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        else:
            self.change_text(self.text)

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
        self.shop_button = Button("SHOP", font,
                                  (400 * scr_w, 100 * scr_h),
                                  (1470 * scr_w, 50 * scr_h))
        self.logo = logo
        self.bg = bg
        self.enabled = True

    def show(self):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        scaled_logo = pygame.transform.scale(self.logo, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_logo, (0, 0))
        self.start_button.show()
        self.exit_button.show()
        self.exit_button.click()
        self.start_button.click()
        self.shop_button.show()
        self.shop_button.click()

    def update_animation(self):
        pass

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


class ShopMenu:
    def __init__(self, scr_w, scr_h, bg, font, bought_cars, player):
        self.prev_car = Button("<--", font,
                               (400 * scr_w, 100 * scr_h),
                               (300 * scr_w, 400 * scr_h))
        self.next_car = Button("-->", font,
                               (400 * scr_w, 100 * scr_h),
                               (1200 * scr_w, 400 * scr_h))
        self.back_button = Button("BACK", font,
                                  (400 * scr_w, 100 * scr_h),
                                  (50 * scr_w, 50 * scr_h))
        self.buy_button = Button("BUY", font,
                                 (300 * scr_w, 100 * scr_h),
                                 (800 * scr_w, 1000 * scr_h))

        self.price_list = self.load_price_list()
        self.shop_items = list(self.price_list.keys())
        self.bought_cars = bought_cars
        self.player = player
        self.bg = bg
        self.enabled = False

    def show(self, money, car):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        car.update()
        car.draw(display.screen)

        self.prev_car.show()
        self.next_car.show()
        self.buy_button.show()
        self.back_button.show()

        self.back_button.click()
        self.next_car.click()
        self.buy_button.click()
        self.prev_car.click()
        # if self.police_car.bought:
        #     self.police_car.text = "POLICE"
        #     self.police_car.click()
        # else:
        #     if money >= 200:
        #         self.police_car.click()

    def change_shop_item(self, destination):
        pass

    def buy(self, money, car):
        car = car.tag
        price = int(self.price_list[car])
        if money >= price and car not in self.bought_cars:
            self.bought_cars.append(car)
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
