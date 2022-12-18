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
        self.bought = False
        self.render = None

    def change_text(self, text, bg="white"):
        self.render = self.font.render(text, 1, pygame.Color("Black"))
        self.surface.fill(bg)
        self.surface.blit(self.render, (self.width // 2 - 50, self.height // 2 - 30))

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

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


class ShopMenu:
    def __init__(self, scr_w, scr_h, bg, font):
        self.red_car = Button("RED", font,
                              (400 * scr_w, 200 * scr_h),
                              (400 * scr_w, 400 * scr_h))
        self.police_car = Button("200 $", font,
                                 (400 * scr_w, 200 * scr_h),
                                 (1200 * scr_w, 400 * scr_h))
        self.back_button = Button("BACK", font,
                                  (400 * scr_w, 100 * scr_h),
                                  (50 * scr_w, 50 * scr_h))
        self.bg = bg
        self.enabled = False

    def show(self, money, car):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        car.update()
        car.draw(display.screen)

        self.red_car.show()
        self.police_car.show()
        self.back_button.show()
        self.back_button.click()
        self.red_car.click()
        if self.police_car.bought:
            self.police_car.text = "POLICE"
            self.police_car.click()
        else:
            if money >= 200:
                self.police_car.click()

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
