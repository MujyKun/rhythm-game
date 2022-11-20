import ppb
from ppb.features.default_sprites import TargetSprite


class Ship(TargetSprite):
    target = ppb.Vector(0, 40)


def setup(scene):
    scene.add(Ship(position=(0, -7)))


if __name__ == '__main__':
    ppb.run(setup=setup)