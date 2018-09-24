import random
from pathlib import PurePath

from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.helpers import sort_hand
from schafkopf.suits import *
from schafkopf.game_modes import *

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition


SUITS = {"0": "Schellen", "1": "Herz", "2": "Gras", "3": "Eichel"}
SYMBOLS = {"0": "7", "1": "8", "2": "9", "3": "U", "4": "O", "5": "K", "6": "10", "7": "A"}


class MyScreenManager(ScreenManager):

    def __init__(self, playerlist):
        ScreenManager.__init__(self)
        self.leading_player_index = random.choice(range(4))
        self.playerlist = playerlist
        self.current_game_state = None

    def new_game(self):
        player_hands = CardDeck().shuffle_and_deal_hands()
        player_index = 0
        hand = sort_hand(player_hands[player_index])
        screen = self.get_screen('playing_screen')
        for card, widget in zip(hand, screen.ids.cards.children):
            im_name = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
            filepath = PurePath('..', 'images', im_name)
            widget.source = str(filepath)
        self.current = 'playing_screen'
        self.current_game_state = self.new_game_state(player_hands)

    def new_game_state(self, player_hands):
        game_state = {'player_hands': player_hands,
                      'leading_player_index': self.leading_player_index,
                      'current_player_index': self.leading_player_index,
                      'mode_proposals': [],
                      'game_mode': (NO_GAME, None),
                      'trumpcards': [],
                      'declaring_player': None,
                      'tricks': [],
                      'current_trick': None}
        return game_state


class MenuScreen(Screen):
    pass


class PlayingScreen(Screen):
    def print_msg(self, string):
        print(string)


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


class SchafkopfApp(App):
    def build(self):
        playerlist = []
        return MyScreenManager(playerlist)


if __name__ == '__main__':
    tut_app = SchafkopfApp()
    tut_app.run()
