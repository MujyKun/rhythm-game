import logging

import ppb
from models import Player, Label, FPSScene, Floor, Note, Song

RES = (1080, 720)


def setup(scene: ppb.Scene):
    scene.background_color = (255, 255, 255)

    # note = Note("a", 4)
    # scene.add(note)

    test_song = Song.load("assets/testsong.json")

    test_song.play(scene, volume=0.1)
    sprites = [

        Floor(
            position=(0, -8), image_location="assets/floor.png", width=30),
        Player(
            position=(5, 5),
            vertical_movement=False,
            horizontal_movement=True,
            jump_movement=True,
            player_type="green"
        ),
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
