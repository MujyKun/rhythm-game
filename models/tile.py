import ppb
from ppb import keycodes, Vector
from ppb.sprites import RectangleSprite, RectangleShapeMixin
from ppb.events import KeyPressed, KeyReleased, PlaySound


class Tile(RectangleSprite):
    """
    A Tile sprite. Represents a tile.

    Parameters
    ----------
    position: tuple
        The position the tile should start at.
    image_location: str
        The location of the image.
    height: int
        Height of the tile.
    width: int
        Width of the tile.
    """
    def __init__(self, position: tuple = None, width=None, height=None, image_location="assets/default.png", **kwargs):
        super(Tile, self).__init__(**kwargs)
        if width:
            self.width = width
        if height:
            self.height = height
        self.position = Vector(*position)
        self.image = ppb.Image(image_location)
