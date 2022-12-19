import pygame
import random


class Road:
    def __init__(self, display, car):
        self.display = display
        self.car = car
        self.speed = 5
        self.rect = pygame.Rect((500 * display.scr_w, 0, 920 * display.scr_w, display.screen_height))
        self.obstacle1 = Obstacles(display, random.randrange(int(500 * display.scr_w), int((1420 - 200) * display.scr_w)), car)
        self.obstacle2 = Obstacles(display, random.randrange(int(500 * display.scr_w), int((1420 - 200) * display.scr_w)), car)
        self.line_list = []
        for i in range(4):
            roadline = RoadLine(display, 0 + (i * 300 * display.scr_h), car, self.speed)
            self.line_list.append(roadline)

    def generate(self):
        for i in self.line_list:
            i.move(self.speed)
            i.draw(self.display.screen)
        if self.obstacle1.rect.top < self.display.screen_height or self.obstacle2.rect.top < self.display.screen_height:
            self.obstacle1.move(self.speed)
            self.obstacle2.move(self.speed)
            self.obstacle1.draw(self.display.screen)
            self.obstacle2.draw(self.display.screen)
        else:
            self.obstacle1 = Obstacles(self.display, random.randrange(int(500 * self.display.scr_w), int((1420 - 200) * self.display.scr_w)), self.car)
            self.obstacle2 = Obstacles(self.display, random.randrange(int(500 * self.display.scr_w), int((1420 - 200) * self.display.scr_w)), self.car)


class Obstacles:
    def __init__(self, display, x, target):
        self.display = display
        self.rect = pygame.Rect((x, 0 - 200 * display.scr_h, 200 * display.scr_w, 200 * display.scr_h))
        self.target = target

    def move(self, speed):
        # update obstacle position
        if self.target.alive:
            self.rect.y += speed
            if self.target.rect.colliderect(self.rect) and self.target.hit_cooldown <= 0:
                self.target.hit = True
                self.target.health -= 20
                self.target.hit_cooldown = 80

    def draw(self, surface):
        # img = pygame.transform.flip(self.image, False, False)
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
        # surface.blit(img,
        #       (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))


class RoadLine:
    def __init__(self, display, y, target, speed):
        self.display = display
        self.rect = pygame.Rect((940 * display.scr_w, y - 200, 50 * display.scr_w, 100 * display.scr_h))
        self.target = target

    def move(self, speed):
        # update obstacle position
        if self.target.alive:
            self.rect.y += speed
            if self.rect.top > self.display.screen_height:
                self.rect.y = 0 - 200

    def draw(self, surface):
        # img = pygame.transform.flip(self.image, False, False)
        pygame.draw.rect(surface, (255, 255, 255), self.rect)


