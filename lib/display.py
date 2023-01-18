import pygame

from const.CONSTANTS import *


class Display:
    def __init__(self):
        # Нативное разрешение пользователя
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)
        # self.screen_width = 1600
        # self.screen_height = 900

        # Разрешение экрана для pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Разрешение в сравнении с нативным
        self.scr_w = self.screen_width / 1920
        self.scr_h = self.screen_height / 1080

        # Получение окна
        self.get_screen()

        # Заголовок окна
        self.set_caption("Mutual Meter")

    def get_screen(self):
        return self.screen

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    # function for drawing text
    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    # function for drawing bg
    def draw_bg(self, bg):
        scaled_bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
        self.screen.blit(scaled_bg, (0, 0))

    # function to draw health bars
    def draw_health_bar(self, health, x, y, heart_sprite, max_health):
        ratio = health / 100
        pygame.draw.rect(self.screen, (255, 255, 255), (x - 2, y - 2, (max_health * 4) + 4 * SCREEN_WIDTH, 34 * SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, (max_health * 4) * SCREEN_WIDTH, 30 * SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y + 15, (max_health * 4) * SCREEN_WIDTH, 15 * SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (250, 200, 0), (x, y, 400 * ratio * SCREEN_WIDTH, 30 * SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (195, 155, 0), (x, y + 20, 400 * ratio * SCREEN_WIDTH, 10 * SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 0), (x, y, 400 * ratio * SCREEN_WIDTH, 10 * SCREEN_HEIGHT))
        img = pygame.transform.scale(heart_sprite, (50, 50))
        self.screen.blit(img, (10, 16))

    def draw_hit_cooldown(self, hit_colodown, shield_sprite):
        img = pygame.transform.scale(shield_sprite, (45, 45))
        self.screen.blit(img, (10, 56))
        pygame.draw.rect(self.screen, (23, 51, 250), (65, 60, hit_colodown, 30))

    def draw_image(self, image, size, coords):
        img = pygame.transform.scale(image, size)
        self.screen.blit(img, coords)
