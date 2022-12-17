import pygame
import random


class Road:
    def __init__(self, display, car):
        self.display = display
        self.car = car
        self.speed = 5
        self.rect = pygame.Rect((500 * display.scr_w, 0, 920 * display.scr_w, display.screen_height))
        self.obstacle1 = Obstacles(display, random.randrange(500, 1420 - 200), car, self.speed)
        self.obstacle2 = Obstacles(display, random.randrange(500, 1420 - 200), car, self.speed)

    def generate(self):
        if self.obstacle1.rect.top < self.display.screen_height or self.obstacle2.rect.top < self.display.screen_height:

            self.obstacle1.move()
            self.obstacle2.move()
            self.obstacle1.draw(self.display.screen)
            self.obstacle2.draw(self.display.screen)
        else:
            self.obstacle1 = Obstacles(self.display, random.randrange(500, 1420 - 200), self.car, self.speed)
            self.obstacle2 = Obstacles(self.display, random.randrange(500, 1420 - 200), self.car, self.speed)


class Obstacles:
    def __init__(self, display, x, target, speed):
        self.display = display
        self.rect = pygame.Rect((x, 0 - 200 * display.scr_h, 200 * display.scr_w, 200 * display.scr_h))
        self.target = target
        self.speed = speed

    def move(self):
        # update obstacle position
        self.rect.y += self.speed
        if self.target.rect.colliderect(self.rect) and self.target.hit_cooldown <= 0:
            self.target.health -= 50
            self.target.hit_cooldown = 80

    def draw(self, surface):
        # img = pygame.transform.flip(self.image, False, False)
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
        # surface.blit(img,
        #       (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))
