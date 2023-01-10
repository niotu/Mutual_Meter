from pygame import mixer

mixer.init()

# Класс саунда и музыка миксера
music = mixer.music
sound = mixer.Sound
VOLUME = 0.2
SOUND_VOLUME = VOLUME + 0.2


# Воспроизводство фоновой музыки
def play_music(music_bg):
    music.stop()
    music.load(music_bg)
    music.set_volume(VOLUME)
    music.play(-1)


def change_volume(n):
    global VOLUME
    VOLUME += n
    music.set_volume(VOLUME)


def get_volume():
    return VOLUME
