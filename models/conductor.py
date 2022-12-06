import ppb
from ppb import keycodes
import ext.ext_events
from models import Song
from ext import Music


class Conductor(ppb.Sprite):
    """
    A conductor of the music. Represents a controller to keep update() and the music in sync.

    Parameters
    ----------
    song_file_location: str
        The song file location that is to be loaded and managed.
    music_name: str
        The music filename that is to be loaded and played.
    bpm: int
        The beat per minute of the song.
    floor_height: float
        Height to generate beat zones.

    Attributes
    ----------
    song: models.Song
        The Song that is currently being managed.
    music: ext.Music
        The Music that is to be played with the song.
    bpm: int
        The beat per minute of the song.
    sec_per_beat: float
        The position within the song that is currently playing.
    last_beat: float
        The position within the song that last time a beat was played.
    """

    PLAY = keycodes.L

    def __init__(
        self,
        song_file_location,
        music_name="assets/default.wav",
        bpm=100,
        floor_height: float = None,
        autoplay=False
    ):
        super(Conductor, self).__init__()
        self.image = None
        self.song = Song.load(song_file_location, floor_height=floor_height, autoplay=autoplay)
        self.music = Music(music_name)
        self.music.volume = 0.05
        self.bpm = bpm
        self.sec_per_beat = 60 / self.bpm
        self.last_beat = 0
        self.playing = False
        self._beat = ppb.events.PlaySound(ppb.Sound("assets/beat_1.wav"))
        self._beat.sound.volume = 0.05

    def start(self, scene, volume=0.1, tile_speed=1):
        """Start Song object and set up beat variables"""
        self.playing = True
        self.last_beat = 0
        self.song.play(scene=scene, bpm=self.bpm, volume=volume, tile_speed=tile_speed)

    def get_last_diff_time(self):
        """Return the difference between the last beat and the current time in the playing song"""
        return self.music.music_position - self.last_beat

    def get_next_diff_time(self):
        """Return the difference between the next beat and the current time in the playing song"""
        next_beat = self.last_beat + self.sec_per_beat
        return next_beat - self.music.music_position

    def on_update(self, event, signal):
        if self.music.music_position > self.last_beat + self.sec_per_beat:
            # signal(self._beat)
            self.last_beat += self.sec_per_beat
        self.song.current_beat_in_seconds = self.music.music_position

    def on_key_pressed(self, key_event: ppb.events.KeyPressed, signal):
        if key_event.key == self.PLAY:
            signal(ext.ext_events.PlayMusic(self.music))
            signal(ext.ext_events.StartVis())
            self.start(key_event.scene, volume=1, tile_speed=7)

            from models import Player
            for player in key_event.scene.get(kind=Player):
                player.reset()

