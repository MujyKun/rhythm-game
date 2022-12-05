from typing import Optional

import ppb
from ppb import keycodes, Sprite, Vector
from ppb.camera import Camera
from ppb.events import KeyPressed, KeyReleased
from ppb.features.animation import Animation
from . import Floor, Label, is_colliding


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
    player_type: str
        The player type. Can be found as a folder name in assets/player
        Examples include: naked, green
    scrollable_camera: bool
        Whether the camera will scroll based on the player location.
    zoom_camera: bool
        Whether the camera can be zoomed in/out by the player.
    move_outside_camera: bool
        Whether the player is able to move outside of the camera.
    several_jumps: bool
        Whether the player can jump several times at once.

    Attributes
    ----------
    position: tuple
        The player's position.
    direction: tuple
        The player's headed direction.
    pressed_keys: List[ppb.keycodes.KeyCode]
        A list of key codes that are currently being pressed.
    """

    LEFT = keycodes.A
    RIGHT = keycodes.D
    UP = keycodes.W
    DOWN = keycodes.S
    JUMP = keycodes.Space
    ZOOM_IN = keycodes.Equals
    ZOOM_OUT = keycodes.Minus
    # GRAVITY = 0.8 # Moon Gravity
    GRAVITY = 1.8  # Earth Gravity
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
        player_type="naked",
        move_outside_camera=True,
        several_jumps=False,
        max_health=10
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
        # self.image = ppb.Image(image_location)
        # self.image = Animation("assets/player/left_walk/{0..8}.png", 8)
        self._folder_name = f"assets/player/{player_type}/"
        self._left_walk_animation = Animation(
            self._folder_name + "left_walk/{0..8}.png", 8
        )
        self._right_walk_animation = Animation(
            self._folder_name + "right_walk/{0..8}.png", 8
        )
        self._stand_image = ppb.Image(self._folder_name + "stand_still/0.png")

        self.image = None
        self.stand_still()
        self.sound_playing = False
        self._zoom_camera = zoom_camera
        self._scrollable_camera = scrollable_camera
        self.scene = None
        self.pressed_keys = []
        self._direction_walking = None
        self._move_outside_camera = move_outside_camera
        self._several_jumps = several_jumps
        self.layer = 4
        self.max_health = max_health
        self.hits = 0
        self.misses = 0
        self._health_label = None
        self._accuracy_label = None

    @property
    def camera(self) -> Optional[Camera]:
        """Get the scene camera."""
        if not self.scene:
            return

        if not self.scene.main_camera:
            return

        camera: Camera = self.scene.main_camera
        return camera

    @property
    def health(self):
        return self.max_health - self.misses

    @property
    def accuracy(self):
        total = self.hits + self.misses
        if total != 0:
            return self.hits / (self.hits + self.misses)
        else:
            return 1.00

    def reset(self):
        self.hits = 0
        self.misses = 0
        self.max_health = 10

    def walk_left(self):
        """Make the animation walk left."""
        self._direction_walking = self.LEFT
        self.image = self._left_walk_animation

    def walk_right(self):
        """Make the animation walk right."""
        self._direction_walking = self.RIGHT
        self.image = self._right_walk_animation

    def stand_still(self):
        """Make the animation stand still."""
        self._direction_walking = None
        self.image = self._stand_image

    def on_update(self, event, signal):
        scene = self.scene = event.scene
        # Update the health/accuracy label
        if self._health_label and self._accuracy_label:
            scene.remove(self._health_label)
            scene.remove(self._accuracy_label)
        self._health_label = Label(f"Health: {self.health}", size=50)
        self._accuracy_label = Label(f"Accuracy: {round(self.accuracy, 2):.2f}", size=50)
        health_x, health_y = scene.main_camera.top_left
        self._health_label.position = Vector(health_x+2, health_y-2.5)
        self._accuracy_label.position = Vector(health_x+2.9, health_y-3.5)
        scene.add(self._health_label)
        scene.add(self._accuracy_label)

        self.direction += Vector(0, -self.GRAVITY) * event.time_delta

        for floor in scene.get(kind=Floor):
            if is_colliding(self, floor):
                if self.direction[1] <= 0:
                    self.direction = Vector(self.direction[0], 0)

        self.position += self.direction * self.speed * event.time_delta

        if not self._move_outside_camera:
            self._check_wall_boundaries()

        if self._scrollable_camera:
            # update our camera location
            self._adjust_camera()

        # handle keys that are currently being held down.
        [self.on_key_held(key) for key in self.pressed_keys]
        self._handle_animation()

    def _check_wall_boundaries(self):
        """Move the player within camera range if they move outside of the camera range."""
        if not self.camera:
            return

        if self.camera.sprite_in_view(self):
            return

        dx, dy = self.direction

        if self.position.x > self.camera.right and dx > 0:  # right wall
            self.position = Vector(self.camera.right, self.position.y)
        if self.position.x < self.camera.left and dx < 0:  # left wall
            self.position = Vector(self.camera.left, self.position.y)

        if self.position.y > self.camera.top and dy > 0:  # top wall
            self.position = Vector(self.position.x, self.camera.top)
        if self.position.y < self.camera.bottom and dy < 0:  # bottom wall
            self.position = Vector(self.position.x, self.camera.bottom)

    def _handle_animation(self):
        """Handle the animations for walking based on the velocity."""
        horizontal_movement = self.direction[0]
        if horizontal_movement < 0 and self._direction_walking != self.LEFT:
            self.walk_left()
        elif horizontal_movement > 0 and self._direction_walking != self.RIGHT:
            self.walk_right()
        elif horizontal_movement == 0 and self._direction_walking:
            self.stand_still()

    def _adjust_camera(self):
        """Adjust the camera to keep the player in a scrolling view."""
        if not self.camera or self.camera.sprite_in_view(self):
            return

        if self.right > self.camera.right:
            self.camera.left = self.right
        elif self.left < self.camera.left:
            self.camera.right = self.left

        if self.top > self.camera.top:
            self.camera.bottom = self.top
        elif self.bottom < self.camera.bottom:
            self.camera.top = self.bottom

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
                jump_vec = Vector(0, self.MOVEMENT_AMPLITUDE)
                if self._several_jumps:
                    self.direction += jump_vec
                else:
                    touching_floor = False
                    for floor in self.scene.get(kind=Floor):
                        if is_colliding(self, floor):
                            touching_floor = True
                    if touching_floor:
                        self.direction += jump_vec

    def _control_camera_movement(self, key):
        """Control the camera movement decided by the player."""
        if not self._zoom_camera:
            return

        if not self.camera:
            return

        if key == self.ZOOM_IN:
            self.camera.height -= self.ZOOM_AMPLITUDE
            self.camera.width -= self.ZOOM_AMPLITUDE
        elif key == self.ZOOM_OUT:
            self.camera.height += self.ZOOM_AMPLITUDE
            self.camera.width += self.ZOOM_AMPLITUDE

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
