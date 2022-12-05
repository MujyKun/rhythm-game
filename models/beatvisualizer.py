import ppb

from ppb import Sprite, RectangleSprite, Rectangle, Vector
from ppb.assetlib import AbstractAsset
from models import Conductor


class BeatVisualizer(object):
    """
    A beat visualizer. Displays the beat of the song that is currently playing.

    Parameters
    ----------
    size: int
        The size of the middle target that the triggers are moving towards.
    position: tuple
        The position of the middle target.
    image: AbstractAsset
        The image of the middle target.
    trigger_image: AbstractAsset
        The image of the triggers.
    bpm: int
        The beat per minute of the song currently playing.
    Attributes
    ----------
    position: tuple
        The position of the middle target.
    """

    def __init__(
        self,
        size: int = 1,
        position: tuple = None,
        image: AbstractAsset = None,
        trigger_image: AbstractAsset = None,
        bpm: int = 100,
    ):
        position = position or (0, 0)
        self.bpm = bpm

        # Initialize the middle target box
        image = image or ppb.Square(200, 200, 100)

        self.target_box = Sprite(size=size, position=position, image=image)
        self.target_box.rotate(45)
        self.target_box.layer = 2

        # Initialize the triggers
        self.left_triggers = []
        self.right_triggers = []

        for i in range(0, 5):
            self.left_triggers.append(
                BeatTrigger(
                    width=0.25,
                    height=0.5,
                    position=(
                        self.target_box.position.x - 10 + i * 2,
                        self.target_box.position.y,
                    ),
                    direction=(1, 0),
                    image=trigger_image,
                    layer=self.target_box.layer + 1,
                    bpm=self.bpm,
                )
            )
            self.right_triggers.append(
                BeatTrigger(
                    width=0.25,
                    height=0.5,
                    position=(
                        self.target_box.position.x + 10 - i * 2,
                        self.target_box.position.y,
                    ),
                    direction=(-1, 0),
                    image=trigger_image,
                    layer=self.target_box.layer + 1,
                    bpm=self.bpm,
                )
            )

    def setup(self, scene):
        scene.add(self.target_box)
        for trigger in self.left_triggers:
            scene.add(trigger)
        for trigger in self.right_triggers:
            scene.add(trigger)


class BeatTrigger(RectangleSprite):
    """
    A "trigger" for the beat visualizer. Once hit middle, play inputs action.

    Parameters
    ----------
    width: float
        The width of the trigger.
    height: float
        The height of the trigger.
    position: tuple
        How far away is the trigger from the middle target.
    direction: tuple
        In what direction is the trigger going.
    image: AbstractAsset
        The image of the trigger to be drawn.
    layer: int
        The layer (one above the target) where the trigger will be drawn.
    bpm: int
        The bpm of the song that is currently playing to calculate the speed.

    Attributes
    ----------
    width: int
        The width of the trigger.
    height: int
        The height of the trigger.
    position: tuple
        How far away is the trigger from the middle target.
    direction: tuple
        In what direction is the trigger going.
    image: AbstractAsset
        The image of the trigger to be drawn.
    """

    def __init__(
        self,
        width: float = None,
        height: float = None,
        position: tuple = None,
        direction: tuple = None,
        image: AbstractAsset = None,
        layer=0,
        bpm=150,
    ):
        super(BeatTrigger, self).__init__()
        position = position or (0, 0)
        direction = direction or (0, 0)
        self.width = width or 1
        self.height = height or 1
        self.position = Vector(*position)
        self.direction = Vector(*direction)
        # The starting position is the 10 out going in the opposite direction
        self._start_pos_x = 10 * self.direction.x * -1
        self._start_pos_y = self.position.y
        self.start_pos = Vector(self._start_pos_x, self._start_pos_y)
        # Calculating how fast the triggers should go to stay within beat.
        # Because this using seconds instead of time, it will go out of sync if
        # frame rate is not constant.
        self.bpm = bpm
        self.speed = 2 / (60 / self.bpm)
        self.image = image or Rectangle(255, 255, 255, (1, 2))
        self.layer = layer
        self.paused = True

    def on_update(self, update_event, signal):
        for conduct in update_event.scene.get(kind=Conductor):
            # Update speed if bpm changes
            if conduct.bpm != self.bpm:
                self.bpm = conduct.bpm
                self.speed = 2 / conduct.sec_per_Beat
        if not self.paused:
            # Only move when the song starts
            self.position += self.direction * self.speed * update_event.time_delta
        for t in update_event.scene.get(kind=BeatTrigger):
            if (t.position - self.position).length <= self.width and t != self:
                t.reset()
                self.reset()

    def on_start_vis(self, event, signal):
        self.paused = False

    def reset(self):
        self.position = self.start_pos
