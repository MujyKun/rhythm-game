def check_in_range(value, min_range, max_range) -> bool:
    return min_range <= value <= max_range


def is_colliding(first_sprite, second_sprite) -> bool:
    """
    Check if sprites are colliding with each other.

    :param first_sprite: Sprite
        sprite object to check collision with.
    :param second_sprite: Sprite
        sprite object to check collision with.
    :return: bool
        Whether the sprites are colliding.
    """
    f_top_left_x, f_top_left_y = second_sprite.top_left
    f_bottom_right_x, f_bottom_right_y = second_sprite.bottom_right

    top_left_x, top_left_y = first_sprite.top_left
    bottom_right_x, bottom_right_y = first_sprite.bottom_right

    f_y_vals = f_top_left_y, f_bottom_right_y
    f_x_vals = f_top_left_x, f_bottom_right_x

    x_range = [min(*f_x_vals), max(*f_x_vals)]
    y_range = [min(*f_y_vals), max(*f_y_vals)]

    x_colliding = False
    y_colliding = False
    for x in [top_left_x, bottom_right_x]:
        if check_in_range(x, *x_range):
            x_colliding = True
    for y in [top_left_y, bottom_right_y]:
        if check_in_range(y, *y_range):
            y_colliding = True
    return x_colliding and y_colliding


from .music import Music, MusicController
from .floor import Floor
from .player import Player
from .label import Label
from .fpsscene import FPSScene
from .note import Note
from .song import Song
from .background import Background
from .beatvisualizer import BeatVisualizer
