import ppb
from ppb import keycodes, Sprite, Vector
from ppb.camera import Camera
from ppb.events import KeyPressed, KeyReleased, PlaySound
from . import Tile


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
    jump_movement: bool
        If the player should be able to jump.
        Does not relate to vertical_movement.
    image_location: str
        The location of the image.
    scrollable_camera: bool
        Whether the camera will scroll based on the player location.
    zoom_camera: bool
        Whether the camera can be zoomed in/out by the player.

    Attributes
    ----------
    position: tuple
        The player's position.
    direction: tuple
        The player's headed direction.
    pressed_keys: List[ppb.keycodes.KeyCode]
        A list of key codes that are currently being pressed.
    """

    LEFT = keycodes.Left
    RIGHT = keycodes.Right
    UP = keycodes.Up
    DOWN = keycodes.Down
    JUMP = keycodes.Space
    ZOOM_IN = keycodes.Equals
    ZOOM_OUT = keycodes.Minus
    GRAVITY = 0.8
    MOVEMENT_AMPLITUDE = 1
    ZOOM_AMPLITUDE = 2

    def __init__(
        self,
        position: tuple = None,
        direction: tuple = None,
        horizontal_movement=False,
        vertical_movement=False,
        jump_movement=False,
        scrollable_camera=True,
        zoom_camera=True,
        image_location="assets/default.png",
    ):
        super(Player, self).__init__()
        position = position or (0, 0)
        direction = direction or (0, 0)
        self.position = Vector(*position)
        self.direction = Vector(*direction)
        self.speed = 5
        self._horizontal_movement = horizontal_movement
        self._vertical_movement = vertical_movement
        self._jump_movement = jump_movement
        self.image = ppb.Image(image_location)
        self.sound_playing = False
        self._zoom_camera = zoom_camera
        self._scrollable_camera = scrollable_camera
        self.scene = None
        self.pressed_keys = []

    def on_update(self, event, signal):
        scene = self.scene = event.scene
        for tile in scene.get(kind=Tile):

            if (tile.position - self.position).length <= self.size:
                # TODO: collision detection.
                # event.scene.remove(self)
                return

        self.direction += Vector(0, -self.GRAVITY) * event.time_delta
        self.position += self.direction * self.speed * event.time_delta

        if self._scrollable_camera:
            # update our camera location
            self._adjust_camera(scene.main_camera)

        # handle keys that are currently being held down.
        [self.on_key_held(key) for key in self.pressed_keys]

    def _adjust_camera(self, camera: Camera):
        """Adjust the camera to keep the player in a scrolling view."""
        if not camera or camera.sprite_in_view(self):
            return

        if self.right > camera.right:
            camera.left = self.right
        elif self.left < camera.left:
            camera.right = self.left

        if self.top > camera.top:
            camera.bottom = self.top
        elif self.bottom < camera.bottom:
            camera.top = self.bottom

    def _control_movement(self, key_event, reverse_motion=False):
        """Control the player movement."""
        if self._horizontal_movement:
            if key_event.key == self.LEFT:
                self.direction += (
                    Vector(-self.MOVEMENT_AMPLITUDE, 0)
                    if not reverse_motion
                    else Vector(self.MOVEMENT_AMPLITUDE, 0)
                )
            elif key_event.key == self.RIGHT:
                self.direction += (
                    Vector(self.MOVEMENT_AMPLITUDE, 0)
                    if not reverse_motion
                    else Vector(-self.MOVEMENT_AMPLITUDE, 0)
                )
        if self._vertical_movement:
            if key_event.key == self.UP:
                self.direction += (
                    Vector(0, self.MOVEMENT_AMPLITUDE)
                    if not reverse_motion
                    else Vector(0, -self.MOVEMENT_AMPLITUDE)
                )
            elif key_event.key == self.DOWN:
                self.direction += (
                    Vector(0, -self.MOVEMENT_AMPLITUDE)
                    if not reverse_motion
                    else Vector(0, self.MOVEMENT_AMPLITUDE)
                )
        if self._jump_movement:
            if key_event.key == self.JUMP and not reverse_motion:
                self.direction += Vector(0, self.MOVEMENT_AMPLITUDE)

    def _control_camera_movement(self, key):
        """Control the camera movement decided by the player."""
        if not self._zoom_camera and self.scene and self.scene.main_camera:
            return

        camera: Camera = self.scene.main_camera
        if key == self.ZOOM_IN:
            camera.height -= self.ZOOM_AMPLITUDE
            camera.width -= self.ZOOM_AMPLITUDE
        elif key == self.ZOOM_OUT:
            camera.height += self.ZOOM_AMPLITUDE
            camera.width += self.ZOOM_AMPLITUDE

    def on_key_pressed(self, key_event: KeyPressed, signal):
        """When a key is pressed."""
        self.pressed_keys.append(key_event.key)
        self._control_movement(key_event)
        self._control_camera_movement(key_event.key)

    def on_key_held(self, key):
        """When a key is not released. Not a ppb event."""
        self._control_camera_movement(key)

    def on_key_released(self, key_event: KeyReleased, signal):
        """When a key is released."""
        self.pressed_keys.remove(key_event.key)
        self._control_movement(key_event, reverse_motion=True)
