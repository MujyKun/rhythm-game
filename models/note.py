import ppb
from ppb import Sound, RectangleSprite, Image
from models import Floor, Player


class Note(RectangleSprite):
    """
    A Note sprite. Represents a note for the player to hit.

    Parameters
    ----------
    note_type: str
        The note to create

    Attributes
    ----------
    position: ppb.Vector/tuple
        The position of the Note.
    direction: ppb.Vector/tuple
        The direction the note is heading (usually down).
    """
    def __init__(self, note_type: str):
        super().__init__()
        # Set up img as another variable and image to None
        # so that we can "trick" the render not to render this Sprite.
        # self._img = Image('/assets/' + note_type + '.png')
        self._img = Image('/assets/note.png')
        self.image = None
        self.sound = Sound('/assets/piano-' + note_type + '.wav')
        self.scene = None
        self.position = ppb.Vector(0, 0)
        self.direction = ppb.Vector(0, -1)
        self.speed = 0

    def on_update(self, event, signal):
        if self.visible:
            scene = self.scene = event.scene
            # for floor in scene.get(kind=Floor):
            #     if (floor.position - self.position).length <= self.size:
            #         self.reset()
            #         self.play(signal)
            for play in scene.get(kind=Player):
                if (play.position - self.position).length <= self.size:
                    self.reset()
                    self.play(signal)
            self.position += self.direction * self.speed * event.time_delta

    def reset(self):
        """Resets the floor to a default position and set it to not be visible."""
        self.image = None
        self.position = ppb.Vector(0, 0)
        self.speed = 0

    def start(self, position, speed):
        """
        Starts the note's to move.

        Parameters
        ----------
        position: tuple/ppb.Vector
            Where the Note should be positioned when added.
        speed: int
            The speed of the Note when added.
        """
        self.image = self._img
        self.position = ppb.Vector(*position)
        self.speed = speed

    def play(self, signal):
        """
        Play's this Note's note...

        Parameters
        ----------
        signal: ppb.events.Signal
            The signal to invoke the PlaySound event.
        """
        signal(ppb.events.PlaySound(self.sound))

    def on_key_pressed(self, key_event, signal):
        if not self.visible:
            self.start(position=(5, 5), speed=1)

    @property
    def visible(self):
        return self.image
