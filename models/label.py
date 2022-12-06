from ppb import Sprite, Text, Font


class Label(Sprite):
    def __init__(self, text, font_location="resources/Roboto-Black.ttf", size=12, color=(0, 0, 0)):
        super(Label, self).__init__()
        self._font_location = font_location or "resources/Roboto-Black.ttf"
        self._size = size
        self._text = text
        self._font = Font(font_location, size=size)
        self.image = Text(text, font=self._font, color=color)
        self.layer = 10

    def update_text(self, text):
        self._text = text
        self.image = Text(text, font=self._font)
