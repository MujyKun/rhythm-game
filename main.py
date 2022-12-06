import logging

import ppb
from models import Player, Label, FPSScene, Floor, Note, Song, Background, Conductor
from ext import MusicController

RES = (1080, 720)
# RES = (2560, 1440)
SONG_FILE_LOCATION = "assets/nekozilla.json"
MUSIC_NAME = "assets/nekozilla.mp3"
BPM = 128


def setup(scene: ppb.Scene):
    scene.background_color = (255, 255, 255)

    floor = Floor(
        position=(0, -8), image_location="assets/floor.png", width=30, height=5.5
    )
    sprites = [
        Background(*RES, animate=True),
        Player(
            position=(-8, -3),
            vertical_movement=False,
            horizontal_movement=True,
            jump_movement=True,
            several_jumps=False,
            zoom_camera=False,
            scrollable_camera=True,
            player_type="green",
            move_outside_camera=False,
        ),
        Background.get_moon(),
        Conductor(
            song_file_location=SONG_FILE_LOCATION,
            music_name=MUSIC_NAME,
            bpm=BPM,
            floor_height=floor.top,
            autoplay=True
        ),
        floor,
    ]

    for sprite in sprites:
        scene.add(sprite)


if __name__ == "__main__":
    ppb.run(
        setup=setup,
        title="Rhythm",
        starting_scene=FPSScene,
        log_level=logging.INFO,
        resolution=RES,
        systems=(MusicController,),
    )
