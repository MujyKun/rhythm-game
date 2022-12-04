import ppb
from ppb import RectangleSprite
from ppb.features.animation import Animation


class Background(RectangleSprite):
    """
    A background sprite. Represents the background.

    Parameters
    ----------
    res_width: int
        The width in pixels of the background image.
    res_height: int
        The height in pixels of the background image
    image_location: str
        The path of the image to be used as the background.
    animate: bool
        Whether to animate the background.
    """

    def __init__(
        self,
        res_width=1080,
        res_height=720,
        image_location="assets/background/background.png",
        animate=True,
        **kwargs
    ):
        super(Background, self).__init__(**kwargs)
        self.res_width = res_width
        self.res_height = res_height
        self.position = ppb.Vector(0, 0)
        self.image_location = image_location
        self.image = None
        if animate:
            self.animate()
        else:
            self.unanimate()
        self.layer = 0

    @staticmethod
    def get_moon():
        """Create a moon object."""
        circle = ppb.Circle(255, 255, 255)
        sprite = ppb.RectangleSprite(width=1, height=1, image=circle, position=(0, 0))
        sprite.layer = 1
        return sprite

    def animate(self):
        """Animate the background."""
        self.image = Animation("assets/background/{0..7}.png", 7)

    def unanimate(self):
        """Un-animate the background."""
        self.image = ppb.Image(self.image_location)

    def on_update(self, event, signal):
        # Currently sets the scene's size as the camera's size. Has issue with layers.
        # Want to have this Sprite move with the camera, but currently affects layers.
        scene = event.scene
        if not scene:
            return

        if not scene.main_camera:
            return
        self.width = self.res_width / scene.main_camera.pixel_ratio
        self.height = self.res_height / scene.main_camera.pixel_ratio
