import logging

import ppb
from models import Player, Label, FPSScene, Floor, Note, Song, Background

RES = (1080, 720)
# RES = (2560, 1440)


def setup(scene: ppb.Scene):
    scene.background_color = (255, 255, 255)

    # note = Note("a", 4)
    # scene.add(note)

    test_song = Song.load("assets/testsong.json", scene=scene)

    test_song.play(volume=0.1)
    sprites = [
        Background(*RES, animate=True),
        Floor(
            position=(0, -8), image_location="assets/floor.png", width=30, height=5.5),
        Player(
            position=(-8, -3),
            vertical_movement=False,
            horizontal_movement=True,
            jump_movement=False,
            zoom_camera=False,
            scrollable_camera=True,
            player_type="green",
            move_outside_camera=False
        ),
        Background.get_moon()
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
    )
