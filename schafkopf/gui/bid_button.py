from kivy.uix.button import Button


class BidButton(Button):
    def __init__(self, **kwargs):
        super(BidButton, self).__init__(**kwargs)
        self._callbacks = []
        self.size_hint = 0.2, 0.05
