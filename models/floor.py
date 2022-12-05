import ppb
from ppb import keycodes, Vector
from ppb.sprites import RectangleSprite, RectangleShapeMixin
from ppb.events import KeyPressed, KeyReleased, PlaySound


class Floor(RectangleSprite):
    """
    A Floor sprite. Represents a Floor.

    Parameters
    ----------
    position: tuple
        The position the floor should start at.
    image_location: str
        The location of the image.
    height: float
        Height of the floor.
    width: float
        Width of the floor.
    """

    def __init__(
        self,
        position: tuple = None,
        width=None,
        height=None,
        image_location="assets/default.png",
        **kwargs
    ):
        super(Floor, self).__init__(**kwargs)
        if width:
            self.width = width
        if height:
            self.height = height
        self.position = Vector(*position)
        self.image = ppb.Image(image_location)
        self.layer = 1
