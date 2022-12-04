import ppb
from ppb import Sound, RectangleSprite, Image
from models import Floor, Player, is_colliding


class Note(RectangleSprite):
    """
    A Note sprite. Represents a note for the player to hit.

    Parameters
    ----------
    note_type: str
        The note to create
    play_at: int
        The beat number to play at.

    Attributes
    ----------
    position: ppb.Vector/tuple
        The position of the Note.
    direction: ppb.Vector/tuple
        The direction the note is heading (usually down).
    play_at: int
        The beat the note will play at.
    """
    def __init__(self, note_type: str, play_at: int):
        super().__init__()
        # Set up img as another variable and image to None
        # so that we can "trick" the render not to render this Sprite.
        self._img = Image(f'/assets/tiles/{note_type}.png')
        self.image = None
        self.sound = Sound(f'/assets/piano-{note_type}.wav')
        self.scene = None
        self.position = ppb.Vector(0, 0)
        self.direction = ppb.Vector(0, -1)
        self.speed = 0
        self.play_at = play_at or 0
        self.sound_to_play = ppb.events.PlaySound(self.sound)
        self.layer = 2

    def on_update(self, event, signal):
        if self.visible:
            scene = self.scene = event.scene
            for floor in scene.get(kind=Floor):
                if is_colliding(self, floor):
                    self.reset()

            for player in scene.get(kind=Player):
                if is_colliding(self, player):
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
        Makes the note start moving.

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
        signal(self.sound_to_play)

    # def on_key_pressed(self, key_event, signal):
    #     if not self.visible:
    #         self.start(position=(5, 5), speed=1)

    @property
    def visible(self):
        return self.image
