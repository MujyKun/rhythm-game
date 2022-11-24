import ppb
from . import Label
from ppb import Scene


class FPSScene(Scene):
    reset_duration = 1  # seconds to reset count.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = 0
        self.start_time = ppb.get_time()
        self._frame_label = None
        self._fps_placement = None
        self.sound_playing = False

    @property
    def avg_frame_rate(self):
        """Get the average frame rate of the scene after the reset duration."""
        return self.frames / (ppb.get_time() - self.start_time)

    def on_pre_render(self, event, signal):
        """Increment frame rate before rendering the frame."""
        if ppb.get_time() - self.start_time > self.reset_duration:
            self.start_time = ppb.get_time()
            self.frames = 1
        else:
            self.frames += 1

    def on_update(self, event, signal):
        """Triggers at the update rate."""
        if self._frame_label:
            self.remove(self._frame_label)

        if not self._fps_placement:
            self._fps_placement = (
                -self.main_camera.width / 2 + 2,
                self.main_camera.height / 2 - 0.5,
            )

        self._frame_label = Label(f"{self.avg_frame_rate:.2f} FPS")
        self._frame_label.position = ppb.Vector(self._fps_placement)
        self.add(self._frame_label)
