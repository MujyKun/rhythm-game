import json
from typing import List

import ppb

from . import Note, BeatZone
from random import randint


class Song:
    """
    Represents a song. Should not be created manually.

    Use the load method.

    Parameters
    ----------
    name: str
        The name of the song.
    tiles: List[:ref:`Note`]
        A list of note (tile) objects.
    spread: bool
        Whether the notes should be randomly spread.
        By default, notes will fall into 4 columns.
    height: int
        The height for beat zones to spawn at.

    Attributes
    ----------
    name: str
        The name of the song.
    tiles: List[:ref:`Note`]
        A list of note (tile) objects.
    """

    def __init__(self, name: str, tiles=None, spread=False, height=None):
        self.name: str = name
        self.tiles: List[Note] = tiles or []
        self._spread = spread
        self.current_beat = 0
        self.x_columns = [-4, -2, 2, 4]
        self.beat_zones = self._create_beat_zones(height=height or -4)
        self._floor_height = height

    def _create_beat_zones(self, height):
        """
        Create the beat zones.

        :param height:
            Height to spawn the beat zones.
        :return: List[:ref:`BeatZone`]
            A list of beat zones.
        """
        zones = []
        images = [
            "assets/arrows/left_arrow.png",
            "assets/arrows/down_arrow.png",
            "assets/arrows/up_arrow.png",
            "assets/arrows/right_arrow.png",
        ]
        glow_images = [
            "assets/arrows/left_arrow_glow.png",
            "assets/arrows/down_arrow_glow.png",
            "assets/arrows/up_arrow_glow.png",
            "assets/arrows/right_arrow_glow.png",
        ]
        from ppb import keycodes

        trigger_keys = [keycodes.Left, keycodes.Down, keycodes.Up, keycodes.Right]
        for idx, column in enumerate(self.x_columns, start=0):
            zones.append(
                BeatZone(
                    (column, height + 1),
                    image_location=images[idx],
                    trigger_key=trigger_keys[idx],
                    glow_image_location=glow_images[idx]
                )
            )
        return zones

    @staticmethod
    def load(file_location, spread=False, floor_height=None):
        """
        Load a song

        :param file_location:
            The json file to load.
        :param spread:
            Whether the notes should be randomly spread.
            By default, notes will fall into 4 columns.
        :param floor_height: float
            The floor height to start beat zones at.
        :return: :ref:`Song`
            returns the Song object.
        """
        with open(file_location) as f:
            song = json.load(f)

        song = song["song"]
        all_notes = song.get("tiles")
        tiles = []
        for beat_number, notes_to_play in all_notes.items():
            for note in notes_to_play:
                tiles.append(Note(note, beat_number))
        return Song(
            name=song.get("name"), tiles=tiles, spread=spread, height=floor_height
        )

    def play(self, scene, bpm, volume=0.1, tile_speed=1):
        """Play the song (game) in the scene."""
        self.current_beat = 0
        for beat_zone in self.beat_zones:
            beat_zone.scene = scene
            scene.add(beat_zone)
        self.arrange_tiles(tile_speed=tile_speed, bpm=bpm)
        for tile in self.tiles:
            scene.add(tile)
            tile.start(tile.position, speed=tile_speed, song=self)
            if not tile.is_blank:
                tile.sound_to_play.sound.volume = volume

    def arrange_tiles(self, tile_speed, bpm):
        """
        Arrange the tiles into columns.

        :param tile_speed: float
            The speed the tiles are going.
        :param bpm: int
            Beats per minute of the song.
        """
        beats_occupied = {}
        for tile in self.tiles:
            while True:
                random_column = randint(0, len(self.x_columns) - 1)
                column_data = beats_occupied.get(random_column)
                if column_data and column_data.get(tile.play_at):
                    continue

                beats_occupied[random_column] = {tile.play_at: True}
                tile.position = ppb.Vector(
                    self.x_columns[random_column],
                    tile.calculate_start_height(
                        bpm=bpm, speed=tile_speed, target_height=self._floor_height or 0
                    ),
                )
                break
