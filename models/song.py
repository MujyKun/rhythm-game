import json
from typing import List

import ppb

from . import Note
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

    Attributes
    ----------
    name: str
        The name of the song.
    tiles: List[:ref:`Note`]
        A list of note (tile) objects.
    """

    def __init__(self, name: str, tiles, scene, spread=False):
        self.name: str = name
        self.tiles: List[Note] = tiles or []
        self._spread = spread
        self.scene = scene
        self.arrange_tiles()

    def arrange_tiles(self):
        """Arrange the tiles into columns."""
        # beats_occupied = {}
        # for tile in self.tiles:
        #     while True:
        #         random_column = randint(0, len(self.columns))
        #         beats_occupied.get(random_column)
        #         if beats_occupied and beats_occupied.get(tile.play_at):
        #             continue
        #
        #         beats_occupied[random_column] = {tile.play_at: True}
        #         tile.position = ppb.Vector(random_column, tile.position.y)
        #         break
        ...

    @staticmethod
    def load(file_location, scene, spread=False):
        """
        Load a song

        :param file_location:
            The json file to load.
        :param scene:
            Scene object.
        :param spread:
            Whether the notes should be randomly spread.
            By default, notes will fall into 4 columns.
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
        return Song(name=song.get("name"), tiles=tiles, scene=scene, spread=spread)

    def play(self, volume=0.1):
        """Play the song (game) in the scene."""
        # last_position = ppb.Vector(-5, -5)
        for tile in self.tiles:
            self.scene.add(tile)
            tile.start(tile.position, speed=1)
            # last_position += ppb.Vector(3, 3)
            tile.sound_to_play.sound.volume = volume
