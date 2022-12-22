from ctypes import windll

screen_width = windll.user32.GetSystemMetrics(0)
screen_height = windll.user32.GetSystemMetrics(1)
SCREEN_WIDTH = screen_width / 1920
SCREEN_HEIGHT = screen_height / 1080

SPEED = 20
HEALTH = 100

CAR_SIZE = 83
CAR_SCALE = 7.1 * SCREEN_WIDTH
CAR_OFFSET = [29, 21]
CAR_DATA = [CAR_SIZE, CAR_SCALE, CAR_OFFSET, [3, 3]]

FPS = 60
TICKS = 50