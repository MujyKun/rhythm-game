import ppb
from models import Song, Music


class Conductor(ppb.Sprite):
    """
    A conductor of the music. Represents a controller to keep update() and the music in sync.

    Parameters
    ----------

    Attributes
    ----------

    """

    def __init__(self, song_name):
        super(Conductor, self).__init__()
        self.image = None
        self.song = Song(song_name)
        self.music = Music(song_name)
        self.bpm = 0
        self.sec_per_beat = None
        self.song_position = self.music.music_position
        self.last_beat = None

    def start(self):
        self.sec_per_beat = 60 / self.bpm
        self.last_beat = 0

    def play(self, scene):
        self.song.play(scene=scene)
