import random
from functools import partial
from pathlib import PurePath

from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.helpers import sort_hand
from schafkopf.suits import *
from schafkopf.game_modes import *
from schafkopf.players import RandomPlayer, HeuristicsPlayer, DummyPlayer

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager


SUITS = {'0': 'Schellen', '1': 'Herz', '2': 'Gras', '3': 'Eichel'}
SYMBOLS = {'0': '7', '1': '8', '2': '9', '3': 'U', '4': 'O', '5': 'K', '6': '10', '7': 'A'}
BIDDING_IDS = {(NO_GAME, None): 'no_game', (PARTNER_MODE, ACORNS): 'partner_acorns',
               (PARTNER_MODE, LEAVES): 'partner_leaves', (PARTNER_MODE, BELLS): 'partner_bells',
               (WENZ, None): 'wenz', (SOLO, ACORNS): 'solo_acorns', (SOLO, LEAVES): 'solo_leaves',
               (SOLO, HEARTS): 'solo_hearts', (SOLO, BELLS): 'solo_bells'}

class GameScreenManager(ScreenManager):

    def new_game(self):
        screen = self.get_screen('playing_screen')
        screen.play_new_game()
        self.current = 'playing_screen'



class MenuScreen(Screen):
    pass


class BiddingLayout(GridLayout):
    pass


class PlayingScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.leading_player_index = random.choice(range(4))
        self.playerlist = [DummyPlayer(),
                           HeuristicsPlayer(),
                           HeuristicsPlayer(),
                           HeuristicsPlayer()]
        self.current_game_state = None

    def play_new_game(self):
        # deal and display cards
        player_hands = CardDeck().shuffle_and_deal_hands()
        human_player_index = 0
        hand = sort_hand(player_hands[human_player_index])
        for card, widget in zip(hand, self.ids.cards.children):
            im_name = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
            filepath = PurePath('..', 'images', im_name)
            widget.source = str(filepath)

        self.current_game_state = self.new_game_state(player_hands)
        curr_pl = self.current_game_state['current_player_index']
        game = Game(players=self.playerlist, game_state=self.current_game_state)

        while game.get_current_player() != human_player_index:
            game.next_action()
        self.current_game_state = game.get_game_state()

        # set prop texts before first player decision
        mode_props = self.current_game_state['mode_proposals']

        for prop in mode_props:
            id = 'player{}_proposal'.format(curr_pl)
            if prop[0] == 0:
                self.ids[id].text = 'Weiter'
            else:
                self.ids[id].text = 'I dad spuin!'
            curr_pl = (curr_pl + 1) % 4

        # set on release actions on game mode decision buttons

        legal_actions = game.get_possible_actions()
        print(legal_actions)
        for action in legal_actions:
            action_id = BIDDING_IDS[action]
            self.ids[action_id].bind(on_release=partial(self.print_msg, action_id))


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

    def print_msg(self, string, *args):
        print(string)

    def set_propositiontext(self, text, player_id):
        self.ids[player_id].text = text





class ImageButton(ButtonBehavior, Image):
    pass


class CardWidgetTrickplay(GridLayout):
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
        super(CardWidgetTrickplay, self).add_widget(widget)
        self.do_layout()

    def remove_widget(self, widget):
        super(CardWidgetTrickplay, self).remove_widget(widget)
        self.do_layout()


class SchafkopfApp(App):
    def build(self):
        return GameScreenManager()


if __name__ == '__main__':
    tut_app = SchafkopfApp()
    tut_app.run()
