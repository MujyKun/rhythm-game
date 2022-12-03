import logging

import ppb
from models import Player, Label, FPSScene, Floor, Note

RES = (1080, 720)


def setup(scene: ppb.Scene):
    scene.background_color = (255, 255, 255)

    note = Note("a")
    # scene.add(note)

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
