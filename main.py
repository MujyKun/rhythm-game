import ppb
from models import Player


def setup(scene):
    scene.add(Player(position=(0, 0), vertical_movement=True, horizontal_movement=True, image_location="assets/test1.jpg"))
    scene.add(Player(position=(0, 5), vertical_movement=True, horizontal_movement=True, image_location="assets/fav.png"))
    scene.add(Player(position=(5, 0), vertical_movement=False, horizontal_movement=True))
    scene.add(Player(position=(5, 5), vertical_movement=False, horizontal_movement=True))


if __name__ == '__main__':
    ppb.run(setup=setup, title="Rhythm")
