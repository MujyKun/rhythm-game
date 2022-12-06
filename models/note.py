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
    autoplay: bool
        Whether the tile will autoplay.

    Attributes
    ----------
    position: ppb.Vector/tuple
        The position of the Note.
    direction: ppb.Vector/tuple
        The direction the note is heading (usually down).
    play_at: int
        The beat the note will play at.
    autoplay: bool
        Whether the tile will autoplay.

    """

    def __init__(self, note_type: str, play_at: int, autoplay=False):
        super().__init__()
        # Set up img as another variable and image to None
        # so that we can "trick" the render not to render this Sprite.
        self.name = note_type

        if self.is_blank:
            self._img = Image(f"/assets/tiles/{note_type}.png")
            self.sound = None
            self.sound_to_play = None
        else:
            self._img = Image(f"/assets/tiles/{note_type[0:-1]}.png")
            self.sound = Sound(f"/assets/notes/{note_type}.wav")
            self.sound_to_play = ppb.events.PlaySound(self.sound)

        self.image = None
        self.scene = None
        self.position = ppb.Vector(0, 0)
        self.direction = ppb.Vector(0, -1)
        self.speed = 0
        self.play_at = float(play_at) or 0
        self.layer = 2
        self.song = None
        self.autoplay = autoplay

    @property
    def is_blank(self):
        return 'blank' in self.name

    def on_update(self, event, signal):
        print(self.song.current_beat)
        if self.visible:
            scene = self.scene = event.scene
            for floor in scene.get(kind=Floor):
                if self.autoplay:
                    if self.song.current_beat >= self.play_at:
                        self.reset()
                        self.play(signal)
                else:
                    for player in scene.get(kind=Player):
                        if is_colliding(self, floor):
                            self.reset()
                            player.misses += 1
                        if is_colliding(self, player):
                            self.reset()
                            self.play(signal)
                            player.hits += 1

            self.position += self.direction * self.speed * event.time_delta

    def reset(self):
        """Resets the tile to a default position and set it to not be visible."""
        self.image = None
        self.position = ppb.Vector(0, 0)
        self.speed = 0

    def calculate_start_height(self, bpm, speed, target_height):
        """
        Calculate the start height of the note.

        :param bpm: int
            Beats per minute
        :param speed: int
            Speed of the note.
        :param target_height: float
            The target's height.
        """
        seconds_per_beat = (60 / bpm)
        seconds_to_beat = self.play_at * seconds_per_beat
        # Need to add 0.5 to make the song play on beat.
        return speed * seconds_to_beat + target_height + 0.5

    def start(self, position, speed, song):
        """
        Makes the note start moving.

        Parameters
        ----------
        position: tuple/ppb.Vector
            Where the Note should be positioned when added.
        speed: int
            The speed of the Note when added.
        song: :ref:`Song`
            The song is belongs to.
        """
        self.image = self._img
        self.position = ppb.Vector(*position)
        self.speed = speed
        self.song = song

    def play(self, signal):
        """
        Play's this Note's note...

        Parameters
        ----------
        signal: ppb.events.Signal
            The signal to invoke the PlaySound event.
        """
        if not self.is_blank:
            signal(self.sound_to_play)

    # def on_key_pressed(self, key_event, signal):
    #     if not self.visible:
    #         self.start(position=(5, 5), speed=1)

    @property
    def visible(self):
        return self.image
