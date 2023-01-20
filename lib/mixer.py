from pygame import mixer
from const.CONSTANTS import *

mixer.init()

# Класс саунда и музыка миксера
music = mixer.music
sound = mixer.Sound

# music
menu_music = r"assets\audio\music\sun-araw-horse-steppin.mp3"
game_music = r"assets\audio\music\moon-hydrogen-hotline-miami-soundtrack.mp3"
# sounds
crash_sound_1 = sound(r"assets\audio\effects\crash1.mp3")
crash_sound_2 = sound(r"assets\audio\effects\crash2.mp3")
crash_sounds = [crash_sound_2, crash_sound_1]
powerup_sound = sound(r"assets\audio\effects\powerup.wav")
button_sound = sound(r"assets\audio\effects\button_click.wav")
button_sound.set_volume(1)

# Воспроизводство фоновой музыки
def play_music(music_bg):
    music.stop()
    music.load(music_bg)
    music.set_volume(VOLUME)
    music.play(-1)


