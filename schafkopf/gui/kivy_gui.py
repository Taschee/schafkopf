from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition


class MenuScreen(Screen):
    pass


class PlayingScreen(Screen):
    def print_msg(self, string):
        print(string)
    pass


class MyScreenManager(ScreenManager):
    def new_game_screen(self):
        s = PlayingScreen(name='playing_screen')
        self.add_widget(s)
        return s


class ImageButton(ButtonBehavior, Image):
    pass


class CardWidget(GridLayout):
    def do_layout(self, *args):
        width = self.width
        width_per_child = int(width // 8)
        positions = range(0, 8 * width_per_child, width_per_child)
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
    pass


class SchafkopfApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    tut_app = SchafkopfApp()
    tut_app.run()
