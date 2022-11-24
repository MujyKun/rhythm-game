import logging

import ppb
from models import Player, Label, FPSScene


def setup(scene: ppb.Scene):
    scene.background_color = (255, 255, 255)
    sprites = [
        Player(position=(0, 0), vertical_movement=True, horizontal_movement=True, image_location="assets/test1.jpg"),
        Player(position=(0, 5), vertical_movement=True, horizontal_movement=True, image_location="assets/fav.png"),
        Player(position=(5, 0), vertical_movement=False, horizontal_movement=True),
        Player(position=(5, 5), vertical_movement=False, horizontal_movement=True),
    ]

    sprites[0].add(sprites[1])

    for sprite in sprites:
        scene.add(sprite)


if __name__ == '__main__':
    ppb.run(setup=setup, title="Rhythm", starting_scene=FPSScene, log_level=logging.INFO)
