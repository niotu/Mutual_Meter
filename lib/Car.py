import pygame


class Car:
    def __init__(self, display):
        self.size = 200
        self.health = 100
        self.moving = False
        self.alive = True
        self.rect = pygame.Rect((900, 700, 150 * display.scr_w, 200 * display.scr_h))
        self.display = display
        self.hit_cooldown = 80

    def move(self):
        SPEED = 10
        dx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -SPEED
            self.moving = True
        if key[pygame.K_d]:
            dx = SPEED
            self.moving = True

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

    def draw(self, surface):
        # img = pygame.transform.flip(self.image, False, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        # surface.blit(img,
        #       (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))
