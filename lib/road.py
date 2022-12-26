import random

import pygame

from const.CONSTANTS import *


class Road:
    def __init__(self, display, car, sheets, datas):
        self.display = display
        self.car = car
        self.sheet_list, self.datas = sheets, datas
        self.speed = 5
        self.rect = pygame.Rect((500 * SCREEN_WIDTH, 0, 920 * SCREEN_WIDTH, screen_height))
        self.obstacle1 = self.obstacle2 = None
        self.update_obstacles()
        self.line1_list = []
        self.line2_list = []
        for i in range(4):
            roadline = RoadLine(display, 780 * SCREEN_WIDTH, 0 + (i * 300 * SCREEN_HEIGHT), car)
            self.line1_list.append(roadline)
        for i in range(4):
            roadline = RoadLine(display, 1080 * SCREEN_WIDTH, 0 + (i * 300 * SCREEN_HEIGHT), car)
            self.line2_list.append(roadline)

    def update_obstacles(self):
        match random.choice((1, 2, 3)):
            case 1:
                sheet = self.sheet_list[0]
            case 2:
                sheet = self.sheet_list[1]
            case _:
                sheet = self.sheet_list[2]
        x1 = random.choice([int(560 * SCREEN_WIDTH), int(870 * SCREEN_WIDTH),
                            int(1170 * SCREEN_WIDTH)])
        x2 = random.choice([int(560 * SCREEN_WIDTH), int(870 * SCREEN_WIDTH),
                            int(1170 * SCREEN_WIDTH)])
        self.obstacle1 = Obstacles(self.display, x1,
                                   self.car, sheet, self.datas[1])
        if x2 != x1:
            self.obstacle2 = Obstacles(self.display, x2,
                                       self.car, sheet, self.datas[1])

    def generate(self):
        for i in self.line1_list:
            i.move(self.speed)
            i.draw(self.display.screen)
        for i in self.line2_list:
            i.move(self.speed)
            i.draw(self.display.screen)
        if self.obstacle1.rect.top < self.display.screen_height:
            if self.obstacle2:
                self.obstacle2.move(self.speed)
                self.obstacle2.update()
                self.obstacle2.draw(self.display.screen)
            self.obstacle1.move(self.speed)
            self.obstacle1.update()
            self.obstacle1.draw(self.display.screen)

        else:
            self.update_obstacles()


class Obstacles:
    def __init__(self, display, x, target, sprite_sheet, data):
        self.display = display
        self.rect = pygame.Rect((x, 0 - 200 * SCREEN_HEIGHT, 150 * SCREEN_WIDTH, 200 * SCREEN_HEIGHT))
        self.target = target
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.animation_list = self.load_images(sprite_sheet, self.animation_steps)
        self.action = 0  # 0 - idle, 1 - hit
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.hit = False

    def move(self, speed):
        # update obstacle position
        if self.target.alive:
            self.rect.y += speed
            if self.target.rect.colliderect(self.rect) and self.target.hit_cooldown <= 0:
                self.target.hit = True
                self.hit = True
                self.target.health -= 20
                self.target.hit_cooldown = 80

    def update(self):
        if not self.hit:
            self.update_action(0)
        else:
            self.update_action(1)
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation is finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if the player is dead then end animation
            if self.hit:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update anim sattings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite_sheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def draw(self, surface):
        img = pygame.transform.flip(self.image, False, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))


class RoadLine:
    def __init__(self, display, x, y, target):
        self.display = display
        self.rect = pygame.Rect((x * SCREEN_WIDTH, y - 200, 50 * SCREEN_WIDTH, 100 * SCREEN_HEIGHT))
        self.target = target

    def move(self, speed):
        # update obstacle position
        if self.target.alive:
            self.rect.y += speed
            if self.rect.top > screen_height:
                self.rect.y = 0 - 200

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
