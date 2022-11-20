import ppb
from ppb import keycodes, Sprite, Vector
from ppb.events import KeyPressed, KeyReleased


class Player(Sprite):
    """
    A player sprite. Represents a player playing the game.

    Parameters
    ----------
    position: tuple
        The position the player should start at.
    direction: tuple
        The direction the player should be heading.
    horizontal_movement: bool
        If the player should be able to move horizontally.
    vertical_movement: bool
        If the player should be able to move vertically.
    image_location: str
        The location of the image.

    Attributes
    ----------
    position: tuple
        The player's position.
    direction: tuple
        The player's headed direction.
    """
    left = keycodes.Left
    right = keycodes.Right
    up = keycodes.Up
    down = keycodes.Down

    def __init__(self, position: tuple = None, direction: tuple = None,
                 horizontal_movement=False, vertical_movement=False, image_location="assets/default.png"):
        super(Player, self).__init__()
        position = position or (0, 0)
        direction = direction or (0, 0)
        self.position = Vector(*position)
        self.direction = Vector(*direction)
        self.speed = 5
        self._horizontal_movement = horizontal_movement
        self._vertical_movement = vertical_movement
        self.image = ppb.Image(image_location)

    def on_update(self, update_event, signal):
        self.position += self.direction * self.speed * update_event.time_delta

    def _control_movement(self, key_event, reverse_motion=False):
        if self._horizontal_movement:
            if key_event.key == self.left:
                self.direction += Vector(-1, 0) if not reverse_motion else Vector(1, 0)
            elif key_event.key == self.right:
                self.direction += Vector(1, 0) if not reverse_motion else Vector(-1, 0)
        if self._vertical_movement:
            if key_event.key == self.up:
                self.direction += Vector(0, 1) if not reverse_motion else Vector(0, -1)
            elif key_event.key == self.down:
                self.direction += Vector(0, -1) if not reverse_motion else Vector(0, 1)

    def on_key_pressed(self, key_event: KeyPressed, signal):
        self._control_movement(key_event)

    def on_key_released(self, key_event: KeyReleased, signal):
        self._control_movement(key_event, reverse_motion=True)
