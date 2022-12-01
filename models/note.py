import ppb
from ppb import Sound, RectangleSprite, Image
from models import Tile, Player


class Note(RectangleSprite):
    """
    A Note sprite. Represents a note for the player to hit.

    Parameters
    ----------
    note: String
        The note to create

    Attributes
    ----------
    position: ppb.Vector/tuple
        The position of the Note.
    direction: ppb.Vector/tuple
        The direction the note is heading (usually down).
    visible: bool
        Is the note visible currently?
    """
    def __init__(self, note):
        super().__init__()
        # Set up img as another variable and image to None
        # so that we can "trick" the render note to render this Sprite.
        self.img = Image('/assets/' + note + '.png')
        self.image = None
        self.sound = Sound('/resources/' + note + '.wav')
        self.scene = None
        self.position = ppb.Vector(0, 0)
        self.direction = ppb.Vector(0, -1)
        self.speed = 0
        self.visible = False

    def on_update(self, event, signal):
        if self.visible:
            scene = self.scene = event.scene
            for floor in scene.get(kind=Tile):
                if (floor.position - self.position).length <= self.size:
                    self.reset()
            for play in scene.get(kind=Player):
                if (play.position - self.position).length <= self.size:
                    self.reset()
                    self.play(signal)
            self.position += self.direction * self.speed * event.time_delta

    def reset(self):
        """Resets the tile to a default position and set it to not be visible."""
        self.visible = False
        self.image = None
        self.position = ppb.Vector(0, 0)
        self.speed = 0

    def start(self, position, speed):
        """Starts the note's to move."""
        self.visible = True
        self.image = self.img
        self.position = ppb.Vector(*position)
        self.speed = speed

    """
    Play's this Note's note...
    
    Attributes
    -----------
    signal: ppb.events.Signal
        The signal to invoke the PlaySound event.
    """
    def play(self, signal):
        signal(ppb.events.PlaySound(self.sound))
