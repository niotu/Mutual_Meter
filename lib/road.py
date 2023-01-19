import random

import pygame

from const.CONSTANTS import *


class Road:
    def __init__(self, display, car, sheets, datas):
        self.display = display
        self.car = car
        (self.sheet_list, self.booster_sheets), self.datas = sheets, datas
        self.speed = 5
        self.rect = pygame.Rect((500 * SCREEN_WIDTH, 0, 920 * SCREEN_WIDTH, screen_height))
        self.obstacle1 = self.obstacle2 = None
        self.new_level = False
        self.update_obstacles()
        self.line1_list = []
        self.line2_list = []
        for i in range(4):
            roadline = RoadLine(display, 780 * SCREEN_WIDTH, 0 + (i * 300 * SCREEN_HEIGHT), car)
            self.line1_list.append(roadline)
        for i in range(4):
            roadline = RoadLine(display, 1080 * SCREEN_WIDTH, 0 + (i * 300 * SCREEN_HEIGHT), car)
            self.line2_list.append(roadline)
        self.booster = Booster(self.display, int(870 * SCREEN_WIDTH),
                               self.car, self.booster_sheets[0], self.datas[1], 0)
        self.booster.rect.top = 2000
        self.level = 1

    def update_obstacles(self):
        # нарисовать препятствия сверху экрана
        match random.choice((1, 2, 3)):
            case 1:
                sheet = self.sheet_list[0]
                booster_type = 1
                booster_sheet = self.booster_sheets[0]
            case 2:
                sheet = self.sheet_list[1]
                booster_type = 2
                booster_sheet = self.booster_sheets[1]
            case _:
                sheet = self.sheet_list[2]
                booster_type = 3
                booster_sheet = self.booster_sheets[2]
        line_list = [int(560 * SCREEN_WIDTH), int(870 * SCREEN_WIDTH),
                     int(1170 * SCREEN_WIDTH)]
        x1 = random.choice(line_list)
        x2 = random.choice(line_list)
        if self.new_level:
            self.booster = Booster(self.display, line_list[1],
                                   self.car, booster_sheet, self.datas[1], booster_type)
        else:
            self.obstacle1 = Obstacles(self.display, x1,
                                       self.car, sheet, self.datas[1], 0)
            if x2 != x1:
                self.obstacle2 = Obstacles(self.display, x2,
                                           self.car, sheet, self.datas[1], 0)
        self.new_level = False

    def generate(self, score):
        # нарисовать дорожные линии
        for i in self.line1_list:
            i.move(self.speed)
            i.draw(self.display.screen)
        for i in self.line2_list:
            i.move(self.speed)
            i.draw(self.display.screen)
        # проверка на новый уровень
        if score % 1000 == 0:
            self.level += 1
            self.new_level = True
        # Нарисовать препятствия
        if self.obstacle1.rect.top < self.display.screen_height:
            if self.obstacle2:
                self.obstacle2.move(self.speed)
                self.obstacle2.update()
                self.obstacle2.draw(self.display.screen)
            self.obstacle1.move(self.speed)
            self.obstacle1.update()
            self.obstacle1.draw(self.display.screen)
        elif self.booster.rect.top < self.display.screen_height and self.level != 1:
            self.booster.move(self.speed)
            self.booster.update()
            self.booster.draw(self.display.screen)
        else:
            self.update_obstacles()

    def get_level(self):
        return self.level


class Obstacles:
    def __init__(self, display, x, target, sprite_sheet, data, type):
        self.display = display
        self.rect = pygame.Rect((x, 0 - 200 * SCREEN_HEIGHT, 150 * SCREEN_WIDTH, 200 * SCREEN_HEIGHT))
        self.target = target
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.type = type
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


class Booster(Obstacles):
    def move(self, speed):
        # update obstacle position
        if self.target.alive:
            self.rect.y += speed
            if self.target.rect.colliderect(self.rect) and self.hit is False:
                self.hit = True
                match self.type:
                    case 1:
                        if self.target.health + 20 < self.target.max_health:
                            self.target.health += 20
                        else:
                            self.target.health = self.target.max_health
                    case 2:
                        self.target.hit_cooldown = 200
                    case 3:
                        self.target.double_money_cooldown = 200


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
