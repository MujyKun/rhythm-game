from typing import Optional

import ppb
from ppb import RectangleSprite, Vector, Image
from ppb.events import KeyPressed
from . import is_colliding


class BeatZone(RectangleSprite):
    """
    Is a beat zone that indicates when a tile can be pressed for a column.

    Parameters
    ----------
    position: tuple
        Where the beat zone is located.
    image_location: str
        File location of the image.
    """

    def __init__(self, position: tuple, image_location, trigger_key):
        super(BeatZone, self).__init__()
        self.image = Image(image_location)
        self.width = 2
        self.height = 1
        self.position = Vector(*position)
        self.layer = 3
        self.scene: Optional[ppb.Scene] = None
        self.__KEY = trigger_key

    # def on_key_pressed(self, key_event: KeyPressed, signal):
    #     """When a key is pressed."""
    #     if key_event.key == self.__KEY:
    #         from . import Player  # avoid circular import
    #         for player in self.scene.get(kind=Player):
    #             if is_colliding(self, player):
