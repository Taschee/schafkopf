from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout


class ImageButton(ButtonBehavior, Image):
    pass


class CardWidget(GridLayout):
    def do_layout(self, *args):
        number_of_children = len(self.children)
        width = self.width
        width_per_child = width // 10

        positions = range(width // (number_of_children + 2), 9 * width // (number_of_children + 2), width_per_child)
        for position, child in zip(positions, self.children):
            child.height = self.height
            child.x = self.x + position
            child.y = self.y
            child.width = width_per_child

    def on_size(self, *args):
        self.do_layout()

    def on_pos(self, *args):
        self.do_layout()

    def add_widget(self, widget):
        super(CardWidget, self).add_widget(widget)
        self.do_layout()

    def remove_widget(self, widget):
        super(CardWidget, self).remove_widget(widget)
        self.do_layout()


class BiddingWidget(FloatLayout):
    def print_a(self, string):
        print(string)


class SchafkopfApp(App):
    def build(self):
        return BiddingWidget()


if __name__ == '__main__':
    tut_app = SchafkopfApp()
    tut_app.run()
