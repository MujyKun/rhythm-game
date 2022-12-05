from typing import Optional

import ppb
from ppb import RectangleSprite, Vector, Image
from ppb.events import KeyPressed
import ext.ext_events
from . import is_colliding, check_in_range


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

    def __init__(self, position: tuple, image_location, glow_image_location, trigger_key):
        super(BeatZone, self).__init__()
        self._regular_image = Image(image_location)
        self._glow_image = Image(glow_image_location)
        self.image = self._regular_image
        self.width = 2
        self.height = 1
        self.position = Vector(*position)
        self.layer = 3
        self.scene: Optional[ppb.Scene] = None
        self.__KEY = trigger_key
        self._glowing_since = False
        self._glow_for = 0.25  # how long the zone should glow for.

    def set_regular_image(self):
        """Set the image to its default state."""
        self._glowing_since = None
        self.image = self._regular_image

    def set_glow_image(self):
        """Set the image to its glow state."""
        self._glowing_since = ppb.get_time()
        self.image = self._glow_image

    @property
    def is_glowing(self):
        """Whether the zone is glowing."""
        return bool(self._glowing_since)

    def on_update(self, event, signal):
        if self.is_glowing:
            if ppb.get_time() - self._glowing_since > self._glow_for:
                self.set_regular_image()

    def on_key_pressed(self, key_event: KeyPressed, signal):
        """When a key is pressed."""
        if key_event.key == self.__KEY:
            from . import Player, Conductor, Note  # avoid circular import
            for player in self.scene.get(kind=Player):
                # get time diff
                for conduct in key_event.scene.get(kind=Conductor):
                    time_diff = conduct.get_diff_time()

                # remove/play tile and SCORE
                for tile in key_event.scene.get(kind=Note):
                    if (check_in_range(tile.position.x, self.left, self.right) and
                            check_in_range(tile.position.y, self.bottom-1, self.top+0.5) and
                            time_diff < 0.25):
                        self.set_glow_image()
                        tile.play(signal)
                        tile.reset()
                        player.hits += 1
