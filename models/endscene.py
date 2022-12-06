import ppb.events
from ppb import Scene, keycodes
from models import Label, FPSScene
from main import setup

class EndScene(Scene):

    RESET_KEY = keycodes.L

    def __init__(self):
        super(EndScene, self).__init__()
        self.background_color = (0, 0, 0)
        self.add(Label("GAME OVER", size=50, color=(255, 0, 0)))
        self.replace = False
        self._next_scene = FPSScene()

    def on_update(self, event, signal):
        if self.replace:
            setup(self._next_scene)
            signal(ppb.events.ReplaceScene(self._next_scene))

    def on_key_pressed(self, key_event: ppb.events.KeyPressed, signal):
        if key_event.key == self.RESET_KEY:
            self.replace = True
