from ctypes import windll

screen_width = windll.user32.GetSystemMetrics(0)
screen_height = windll.user32.GetSystemMetrics(1)
SCREEN_WIDTH = screen_width / 1920
SCREEN_HEIGHT = screen_height / 1080

SPEED = 20

CAR_SIZE = 83
CAR_SCALE = 7.1 * SCREEN_WIDTH
CAR_OFFSET = [29, 21]
CAR_DATA = [CAR_SIZE, CAR_SCALE, CAR_OFFSET, [3, 3]]

FPS = 60
TICKS = 50

TAGS_TO_LINKS = {'red_car': r"assets\images\pixel_sprites\car_sprites\car_sprite_sheet.png",
                 'green_car': r'assets\images\pixel_sprites\car_sprites\car_green_sprite_sheet.png',
                 'brown_car': r'assets\images\pixel_sprites\car_sprites\car_brown_sprite_sheet.png',
                 'police_car': r"assets\images\pixel_sprites\car_police_sprite_sheet.png"}
