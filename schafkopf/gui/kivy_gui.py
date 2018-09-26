import random
from functools import partial
from pathlib import PurePath

from kivy.properties import StringProperty
from kivy.uix.button import Button

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
    def __init__(self, playerlist):
        super(GameScreenManager, self).__init__()
        screen = self.get_screen('playing_screen')
        screen.playerlist = playerlist

    def new_game(self):
        screen = self.get_screen('playing_screen')
        screen.play_new_game()
        self.current = 'playing_screen'

class MenuScreen(Screen):
    pass


class BidButton(Button):
    def __init__(self, **kwargs):
        super(BidButton, self).__init__(**kwargs)
        self._callbacks = []
        self.size_hint = 0.2, 0.05


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self._callbacks = []
        self.allow_stretch = True


class PlayingScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayingScreen, self).__init__(**kwargs)
        self.leading_player_index = random.choice(range(4))
        self.current_game_state = None
        self.playerlist = None
        self.human_player_index = 0

    def set_callback(self, callback, btn, *args):
        btn._callbacks.append(callback)
        btn.bind(on_release=callback)

    def clear_callbacks(self, btn, *args):
        while len(btn._callbacks) > 0:
            cb = btn._callbacks[-1]
            btn.unbind(on_release=cb)
            btn._callbacks.remove(cb)

    def play_new_game(self):
        # deal and display cards
        player_hands = CardDeck().shuffle_and_deal_hands()
        self.current_game_state = self.new_game_state(player_hands)

        self.display_human_player_hand()

        curr_pl = self.current_game_state['current_player_index']
        while curr_pl != self.human_player_index:
            # play one action
            game = Game(players=self.playerlist, game_state=self.current_game_state)
            game.next_action()
            self.current_game_state = game.get_game_state()
            # set proposal text in screen ########## maybe do this automatically with some property?
            last_proposal = self.current_game_state['mode_proposals'][-1]
            id = 'player{}_proposal'.format(curr_pl)
            if last_proposal[0] == NO_GAME:
                self.ids[id].text = 'Weiter'
            else:
                self.ids[id].text = 'I dad spuin!'
            curr_pl = self.current_game_state['current_player_index']

        # set on_release actions on game mode decision buttons

        game = Game(players=self.playerlist, game_state=self.current_game_state)
        legal_actions = game.get_possible_actions()
        for action in legal_actions:
            action_id = BIDDING_IDS[action]
            btn = self.ids[action_id]
            self.set_callback(btn=btn, callback=partial(self.make_proposal, action))

    def display_human_player_hand(self):
        hand = sort_hand(self.current_game_state['player_hands'][self.human_player_index])
        for card, widget in zip(hand, self.ids.cards.children):
            im_name = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
            filepath = PurePath('..', 'images', im_name)
            widget.source = str(filepath)

    def make_proposal(self, proposal, *args):
        self.playerlist[self.human_player_index].favorite_mode = proposal
        # update game_state
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        game.next_action()
        self.current_game_state = game.get_game_state()
        # update screen
        id = 'player{}_proposal'.format(self.human_player_index)
        if proposal[0] == 0:
            self.ids[id].text = 'Weiter'
        else:
            self.ids[id].text = 'I dad spuin!'
        # remove bindings
        for btn in self.ids['mode_buttons'].children:
            self.clear_callbacks(btn)
        self.next_opp_proposals()

    def next_opp_proposals(self):
        pass
        game = Game(players=playerlist, game_state=self.current_game_state)
        bidding_ended = game.bidding_game.finished()
        while not bidding_ended:
            if game.get_current_player() != self.human_player_index:
                game.next_action()
                self.current_game_state = game.get_game_state()
                bidding_ended = game.bidding_game.finished()
                # update proposal texts
            else:
                legal_actions = game.get_possible_actions()
                print('player needs to make proposal again!')
                break

        print(self.current_game_state['mode_proposals'])
        print('Bidding ended!')




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
    def __init__(self, playerlist):
        super(SchafkopfApp, self).__init__()
        self.playerlist = playerlist

    def build(self):
        return GameScreenManager(self.playerlist)


if __name__ == '__main__':
    playerlist = [DummyPlayer(), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()]
    tut_app = SchafkopfApp(playerlist)
    tut_app.run()
