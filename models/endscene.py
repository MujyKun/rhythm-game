import ppb.events
from ppb import Scene
from models import Label


class EndScene(Scene):
    def __init__(self):
        super(EndScene, self).__init__()
        self.background_color = (0, 0, 0)
        self.add(Label("GAME OVER", size=50, color=(255, 0, 0)))
