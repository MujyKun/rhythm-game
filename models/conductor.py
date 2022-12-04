import ppb
import ext.music_events
from models import Song
from ext import Music


class Conductor(ppb.Sprite):
    """
    A conductor of the music. Represents a controller to keep update() and the music in sync.

    Parameters
    ----------
    song_name: str
        The song name that is to be loaded and managed.
    music_name: str
        The music filename that is to be loaded and played.
    bpm: int
        The beat per minute of the song.
        
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

    def __init__(self, song_name, music_name="assets/default.wav", bpm=100):
        super(Conductor, self).__init__()
        self.image = None
        self.song = Song.load(song_name)
        self.music = Music(music_name)
        self.music.volume = 0.05
        self.bpm = bpm
        self.sec_per_beat = 0
        self.last_beat = 0
        self.playing = False

    def start(self, scene):
        """Start self.song and set up beat variables"""
        self.playing = True
        self.sec_per_beat = 60 / self.bpm
        self.last_beat = 0
        self.song.play(scene=scene, volume=0.1)

    def on_update(self, event, signal):
        if self.music.music_position > self.last_beat + self.sec_per_beat:
            signal(ppb.events.PlaySound(ppb.Sound('assets/beat_1.wav')))
            print("BANG")
            self.last_beat += self.sec_per_beat

    def on_key_pressed(self, key_event: ppb.events.KeyPressed, signal):
        if key_event.key == ppb.keycodes.L:
            signal(ext.music_events.PlayMusic(self.music))
            self.start(key_event.scene)
