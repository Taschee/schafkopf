from kivy.uix.floatlayout import FloatLayout


class PlayerHandWidget(FloatLayout):
    def do_layout(self, *args):
        width = int(self.width * 0.6)
        height = int(self.height * 0.2)
        width_per_child = int(width // 8)
        start_x = int(0.2 * self.width)
        x_positions = range(start_x, start_x + 8 * width_per_child, width_per_child)
        y_position = self.height * 0.01

        player_card_widgets = self.children

        for position, child in zip(x_positions, player_card_widgets):
            child.height = 0.9 * height
            child.width = 0.9 * width_per_child
            child.x = position
            child.y = y_position

    def on_children(self, *args):
        self.do_layout()

    def on_size(self, *args):
        self.do_layout()

    def on_pos(self, *args):
        self.do_layout()

    def add_widget(self, widget):
        super(PlayerHandWidget, self).add_widget(widget)
        self.do_layout()

    def remove_widget(self, widget):
        super(PlayerHandWidget, self).remove_widget(widget)
        self.do_layout()
