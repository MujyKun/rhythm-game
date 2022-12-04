import ppb
from ppb import RectangleSprite


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
    """
    def __init__(self,
                 res_width=1080,
                 res_height=720,
                 image_location="assets/background.png",
                 **kwargs):
        super(Background, self).__init__(**kwargs)
        self.res_width = res_width
        self.res_height = res_height
        self.position = ppb.Vector(0, 0)
        self.image = ppb.Image(image_location)

    def on_update(self, event, signal):
        # Currently sets the scene's size as the camera's size. Has issue with layers.
        # Want to have this Sprite move with the camera, but currently affects layers.
        scene = event.scene
        self.width = self.res_width / scene.main_camera.pixel_ratio
        self.height = self.res_height / scene.main_camera.pixel_ratio

