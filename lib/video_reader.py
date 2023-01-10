import cv2
import pygame
from lib.display import Display


display = Display()


class VideoReader:
    def __init__(self, bg):
        self.tick = 0
        self.vid = bg
        self.cap = cv2.VideoCapture(self.vid)
        self.ret, img = self.cap.read()
        img = cv2.transpose(img)
        self.surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
        self.scaled_bg = None

    def draw_animated_bg(self):
        if self.tick == 0:
            self.tick = 3
            ret, img = self.cap.read()
            if ret:
                img = cv2.transpose(img)
                pygame.surfarray.blit_array(self.surface, img)
                self.scaled_bg = pygame.transform.scale(self.surface, (850, 550))
                display.screen.blit(self.scaled_bg, (530, 500))

            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                display.screen.blit(self.scaled_bg, (530, 500))
        else:
            self.tick -= 1
            display.screen.blit(self.scaled_bg, (530, 500))
