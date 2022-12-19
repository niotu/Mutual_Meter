import pygame
from const.CONSTANTS import *

class Car:
    def __init__(self, display, data, sprite_sheet, animation_steps):
        self.health = HEALTH
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_steps = animation_steps
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0 - idle, 1 - hit
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.hit = False
        self.alive = True
        self.rect = pygame.Rect((900, 700, 150 * display.scr_w, 200 * display.scr_h))
        self.display = display
        self.hit_cooldown = 80

    def change_skin(self, skin):
        self.sprite_sheet = skin
        self.animation_list = self.load_images(skin, self.animation_steps)

    def move(self):
        dx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED

        if self.rect.left + dx < (500 * self.display.scr_w):
            dx = -self.rect.left + (500 * self.display.scr_w)
        if self.rect.right + dx > self.display.screen_width - (500 * self.display.scr_w):
            dx = self.display.screen_width - (500 * self.display.scr_w) - self.rect.right

        # update player position
        self.rect.x += dx
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        # check if player alive
        if self.health <= 0:
            self.alive = False

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
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 1:
                    self.hit = False

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
