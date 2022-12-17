import pygame
from ctypes import windll

class Display():
    def __init__(self):
        # Нативное разрешение пользователя
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)

        # Разрешение экрана для pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Разрешение в сравнении с нативным
        self.scr_w = self.screen_width / 1920
        self.scr_h = self.screen_height / 1080

        # Получение окна
        self.get_screen()

        # Заголовок окна
        self.set_caption("Великолепное Издание 2: В сердце Японии")
        
    def get_screen(self):
        return self.screen

    def set_caption(self, caption):
        pygame.display.set_caption(caption)