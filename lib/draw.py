import pygame
from lib.display import Display

display = Display()


# function for drawing text
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
