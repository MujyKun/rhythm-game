import ctypes
import faulthandler
import time
import logging
from ppb import Sound
from ppb.systems import SoundController
from ppb.systems.sdl_utils import mix_call, SdlMixerError
from sdl2 import (
    AUDIO_S16SYS,
)
from sdl2.sdlmixer import (
    # Errors, https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_GetError,
    # Support library loading https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_Init,
    Mix_Quit,
    MIX_INIT_FLAC,
    MIX_INIT_MOD,
    MIX_INIT_MP3,
    MIX_INIT_OGG,
    # Mixer init https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_OpenAudio,
    Mix_CloseAudio,
    Mix_QuerySpec,
    # Samples https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_16.html#SEC16
    Mix_LoadMUS,
    Mix_FreeMusic,
    Mix_GetMusicVolume,
    Mix_VolumeMusic,
    # Channels https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_25.html#SEC25
    music_finished,
    Mix_HookMusicFinished,
    Mix_PlayMusic,
    # Other
    MIX_MAX_VOLUME,
    Mix_GetMusicPosition,
)

logger = logging.getLogger(__name__)


def query_spec():
    """
    Helpful wrapper around Mix_QuerySpec()
    Copied from ppb.Sound
    """
    frequency = ctypes.c_int()
    format = ctypes.c_uint16()
    channels = ctypes.c_int()
    count = mix_call(
        Mix_QuerySpec,
        ctypes.byref(frequency),
        ctypes.byref(format),
        ctypes.byref(channels),
        _check_error=lambda rv: rv == 0 and Mix_GetError(),
    )
    return count, frequency, format, channels


class Music(Sound):
    """
    Music. Extends ppb.Sound. Represents a song to play in the music channel.

    Parameters
    ----------
    filename: str
        The filename of the song to create.

    Attributes
    ----------
    volume: int
        The current volume of the song.
    song_position: int
        The current position of the song.
    """

    def _background(self):
        # Called in background thread
        try:
            # Try to open the file to see if it exists
            file = open(self.name)
        except FileNotFoundError:
            if hasattr(self, "file_missing"):
                logger.warning(
                    "File not found: %r. %s", self.name, self.not_found_message
                )
                return self.file_missing()
            else:
                raise
        else:
            # Because we only give the filename as a parameter, close the file
            file.close()
            return self.background_parse(self.name)

    def background_parse(self, name):
        while not any(query_spec()):
            time.sleep(0)
        # Convert str to bytes as this is expected for sdl2
        byte_name = bytes(name, encoding="utf-8")
        return mix_call(Mix_LoadMUS, byte_name, _check_error=lambda rv: not rv)

    def free(self, object, _Mix_FreeMusic=Mix_FreeMusic):
        if object:
            _Mix_FreeMusic(object)

    @property
    def volume(self):
        """
        The volume setting of this chunk, from 0.0 to 1.0
        """
        return mix_call(Mix_GetMusicVolume, self.load()) / MIX_MAX_VOLUME

    @volume.setter
    def volume(self, value):
        mix_call(Mix_VolumeMusic, int(value * MIX_MAX_VOLUME))

    @property
    def music_position(self):
        return mix_call(Mix_GetMusicPosition, self.load())


@music_finished
def _filler_music_finished(music):
    pass


class MusicController(SoundController):
    """
    A controller for Music objects. To be added in the systems parameter of ppb.GameEngine.
    """

    def __enter__(self):
        super().__enter__()
        mix_call(
            Mix_OpenAudio,
            44100,  # Sample frequency, 44.1 kHz is CD quality
            AUDIO_S16SYS,  # Audio, 16-bit, system byte order. IDK is signed makes a difference
            2,  # Number of output channels, 2=stereo
            4096,  # Chunk size. TBH, this is a magic knob number.
            # ^^^^ Smaller is more CPU, larger is less responsive.
            # A lot of the performance-related recommendations are so dated I'm
            # not sure how much difference it makes.
            _check_error=lambda rv: rv == -1,
        )
        mix_call(Mix_Init, MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 | MIX_INIT_OGG)

        logger.debug("MusicController")
        logger.debug(query_spec())

        self.allocated_channels = 16

        # Register callback, keeping reference for later cleanup
        self._finished_callback = music_finished(self._on_channel_finished)
        mix_call(Mix_HookMusicFinished, self._finished_callback)

    def __exit__(self, *exc):
        # Unregister callback and release reference
        mix_call(Mix_HookMusicFinished, _filler_music_finished)
        self._finished_callback = None
        # Cleanup SDL_mixer
        mix_call(Mix_CloseAudio)
        mix_call(Mix_Quit)
        super().__exit__(*exc)

    def on_play_music(self, event, signal):
        faulthandler.enable()
        sound = event.music
        music = event.music.load()
        try:
            music_channel = mix_call(
                Mix_PlayMusic, music, 0, _check_error=lambda rv: rv == -1
            )
        except SdlMixerError as e:
            raise
        else:
            self._currently_playing[music_channel] = sound
