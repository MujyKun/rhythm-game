from ppb import Sprite, Text, Font


class Label(Sprite):
    def __init__(self, text, font_location="resources/Roboto-Black.ttf", size=12):
        super(Label, self).__init__()
        self._font_location = font_location or "resources/Roboto-Black.ttf"
        self._size = size
        self._text = text
        self._font = Font(font_location, size=size)
        self.image = Text(text, font=self._font)

    def update_text(self, text):
        self._text = text
        self.image = Text(text, font=self._font)
