from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self._callbacks = []
        self.allow_stretch = True
