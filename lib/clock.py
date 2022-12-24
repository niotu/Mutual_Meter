import pygame

from const.CONSTANTS import *


class Clock:
    def __init__(self):
        # Клок с фпс лимитом
        self.clock = pygame.time.Clock()
        self.fps = FPS

        # Кулдаун для диалогов
        self.keypress_cooldown = TICKS

        # Тики
        self.ticks = pygame.time.get_ticks()
