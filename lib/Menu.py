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
    def __init__(self, scr_w, scr_h, bg, font):
        self.start_button = Button("START", font,
            (400 * scr_w, 200 * scr_h),
            (1200 * scr_w, 800 * scr_h))
        self.exit_button = Button("EXIT", font,
            (400 * scr_w, 200 * scr_h),
            (400 * scr_w, 800 * scr_h))
        self.bg = bg
        self.enabled = True
        self.is_hide = False

    def show(self):
        if not self.is_hide:
            scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_bg, (0, 0))

            self.start_button.show()
            self.exit_button.show()
            self.exit_button.click()
            self.start_button.click()


    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def hide(self):
        self.is_hide = True

    def show_(self):
        self.is_hide = False