import logging

import ppb
from models import Player, Label, FPSScene, Tile

RES = (1080, 720)


def setup(scene: ppb.Scene):
    scene.background_color = (255, 255, 255)
    sprites = [
        Player(
            position=(5, 5),
            vertical_movement=False,
            horizontal_movement=True,
            jump_movement=True,
            image_location="assets/ball.png",
        ),
        Tile(
            position=(5, -8), image_location="assets/tile.png"),
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
