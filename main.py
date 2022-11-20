import logging

import ppb
from ppb import Scene
from models import Player, Label


class StartingScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frames = 0
        self.start_time = ppb.get_time()
        self._frame_label = None

    @property
    def avg_frame_rate(self):
        """Get the average frame rate of the scene."""
        return self.frames / (ppb.get_time() - self.start_time)

    def on_pre_render(self, event, signal):
        """Increment frame rate before rendering the frame."""
        self.frames += 1

    def on_update(self, event, signal):
        """Triggers at the update rate."""
        if self._frame_label:
            self.remove(self._frame_label)

        self._frame_label = Label(f"{self.avg_frame_rate:.2f} FPS")
        self.add(self._frame_label)


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
    ppb.run(setup=setup, title="Rhythm", starting_scene=StartingScene, log_level=logging.INFO)
