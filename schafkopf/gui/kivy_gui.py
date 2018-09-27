import random
from functools import partial
from pathlib import PurePath
import time

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.helpers import sort_hand
from schafkopf.suits import *
from schafkopf.game_modes import *
from schafkopf.players import RandomPlayer, HeuristicsPlayer, DummyPlayer

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock


SUITS = {'0': 'Schellen', '1': 'Herz', '2': 'Gras', '3': 'Eichel'}
SYMBOLS = {'0': '7', '1': '8', '2': '9', '3': 'U', '4': 'O', '5': 'K', '6': '10', '7': 'A'}
BIDDING_IDS = {(NO_GAME, None): 'no_game', (PARTNER_MODE, ACORNS): 'partner_acorns',
               (PARTNER_MODE, LEAVES): 'partner_leaves', (PARTNER_MODE, BELLS): 'partner_bells',
               (WENZ, None): 'wenz', (SOLO, ACORNS): 'solo_acorns', (SOLO, LEAVES): 'solo_leaves',
               (SOLO, HEARTS): 'solo_hearts', (SOLO, BELLS): 'solo_bells'}
GAME_MODE_TEXTS = {(PARTNER_MODE, ACORNS): 'Auf die Alte!', (PARTNER_MODE, LEAVES): 'Auf die Blaue!',
                   (PARTNER_MODE, BELLS): 'Auf die Schellen!',
                   (WENZ, None): 'Wenz', (SOLO, ACORNS): 'Eichel Solo!', (SOLO, LEAVES): 'Gras Solo',
                   (SOLO, HEARTS): 'Herz Solo', (SOLO, BELLS): 'Schellen Solo'}

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

    def set_proposition_text(self, label_id, text, *args):
        self.ids[label_id].text = text

    def remove_widget_from_display_by_id(self, widget_id, *args):
        self.ids['display'].remove_widget(self.ids[widget_id])

    def add_widget_to_display_by_id(self, widget_id, *args):
        widget = self.ids[widget_id]
        if widget not in self.ids['display'].children:
            self.ids['display'].add_widget(self.ids[widget_id])

    def new_game_state(self, player_hands):
        leading_player_index = random.choice(range(4))
        game_state = {'player_hands': player_hands,
                      'leading_player_index': leading_player_index,
                      'current_player_index': leading_player_index,
                      'mode_proposals': [],
                      'game_mode': (NO_GAME, None),
                      'trumpcards': [],
                      'declaring_player': None,
                      'tricks': [],
                      'current_trick': None}
        return game_state

    def play_new_game(self):
        # deal and display cards
        player_hands = CardDeck().shuffle_and_deal_hands()
        self.current_game_state = self.new_game_state(player_hands)
        # display hand
        self.display_human_player_hand()
        # remove current trick
        self.remove_current_trick_from_display()

        self.start_bidding()

        # set callbacks for legal actions
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        legal_actions = game.get_possible_actions()
        for action in legal_actions:
            action_id = BIDDING_IDS[action]
            btn = self.ids[action_id]
            self.set_callback(btn=btn, callback=partial(self.make_first_proposal, action))

    def start_bidding(self):
        curr_pl = self.current_game_state['current_player_index']
        while curr_pl != self.human_player_index:
            # play one action
            game = Game(players=self.playerlist, game_state=self.current_game_state)
            game.next_action()
            self.current_game_state = game.get_game_state()
            # set proposal text in screen
            last_proposal = self.current_game_state['mode_proposals'][-1]
            label_id = 'player{}_proposal'.format(curr_pl)
            if last_proposal[0] == NO_GAME:
                self.set_proposition_text(label_id, 'Weiter')
            else:
                self.set_proposition_text(label_id, 'I dad spuin!')
            curr_pl = self.current_game_state['current_player_index']

    def remove_current_trick_from_display(self):
        for pl in range(4):
            widget_id = 'player{}_card'.format(pl)
            self.remove_widget_from_display_by_id(widget_id)

    def display_human_player_hand(self):
        hand = sort_hand(self.current_game_state['player_hands'][self.human_player_index])
        for card, widget in zip(hand, self.ids['cards'].children):
            filepath = self.get_filepath(card)
            widget.source = filepath
            widget.text = str(card)

    def get_filepath(self, card):
        im_name = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
        filepath = PurePath('..', 'images', im_name)
        return str(filepath)

    def make_first_proposal(self, proposal, *args):
        self.playerlist[self.human_player_index].favorite_mode = proposal
        # update game_state
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        game.next_action()
        self.current_game_state = game.get_game_state()
        # update screen
        label_id = 'player{}_proposal'.format(self.human_player_index)
        if proposal[0] == NO_GAME:
            self.set_proposition_text(label_id, 'Weiter')
        else:
            self.set_proposition_text(label_id, 'I dad spuin!')
        # remove bindings
        for btn in self.ids['mode_buttons'].children:
            self.clear_callbacks(btn)
        self.finish_first_proposals()

    def finish_first_proposals(self):
        game = Game(players=playerlist, game_state=self.current_game_state)

        while len(self.current_game_state['mode_proposals']) < 4:
            curr_pl = game.get_current_player()
            assert curr_pl != self.human_player_index
            game.next_action()
            self.current_game_state = game.get_game_state()
            label_id = 'player{}_proposal'.format(curr_pl)
            # update proposal texts
            last_proposal = self.current_game_state['mode_proposals'][-1]
            if last_proposal[0] == NO_GAME:
                self.set_proposition_text(label_id, 'Weiter')
            else:
                self.set_proposition_text(label_id, 'I dad spuin!')

        if game.bidding_game.finished():
            self.prepare_trick_play()
        else:
            self.continue_bidding()

    def continue_bidding(self):
        curr_pl = self.current_game_state['current_player_index']
        game = Game(players=self.playerlist, game_state=self.current_game_state)

        if curr_pl == self.human_player_index:
            # set callbacks for legal actions
            legal_actions = game.get_possible_actions()
            for action in legal_actions:
                action_id = BIDDING_IDS[action]
                btn = self.ids[action_id]
                self.set_callback(btn=btn, callback=partial(self.make_second_proposal, action))
        else:
            curr_pl = game.get_current_player()
            game.next_action()
            self.current_game_state = game.get_game_state()
            label_id = 'player{}_proposal'.format(curr_pl)
            # update proposal text
            last_proposal = self.current_game_state['mode_proposals'][-1]
            if last_proposal[0] == NO_GAME:
                self.set_proposition_text(label_id, 'Weiter')
            elif last_proposal[0] == PARTNER_MODE:
                self.set_proposition_text(label_id, 'I hätt a Saupiel!')
            elif last_proposal[0] == WENZ:
                self.set_proposition_text(label_id, 'I hätt an Wenz')
            elif last_proposal[0] == SOLO:
                self.set_proposition_text(label_id, 'I hätt a Solo!')

        if game.bidding_game.finished():
            self.prepare_trick_play()
        else:
            self.continue_bidding()

    def make_second_proposal(self, proposal, *args):
        self.playerlist[self.human_player_index].favorite_mode = proposal
        # update game_state
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        game.next_action()
        self.current_game_state = game.get_game_state()
        # update screen
        label_id = 'player{}_proposal'.format(self.human_player_index)
        if proposal[0] == NO_GAME:
            self.set_proposition_text(label_id, 'Weiter')
        elif proposal[0] == PARTNER_MODE:
            self.set_proposition_text(label_id, 'I hätt a Sauspiel!')
        elif proposal[0] == WENZ:
            self.set_proposition_text(label_id, 'I hätt an Wenz!')
        elif proposal[0] == SOLO:
            self.set_proposition_text(label_id, 'I hätt a Solo!')
        # remove bindings
        for btn in self.ids['mode_buttons'].children:
            self.clear_callbacks(btn)

        self.continue_bidding()

    def prepare_trick_play(self):
        # remove proposal labels for non declarers and display game mode
        dec_pl = self.current_game_state['declaring_player']
        for pl in range(4):
            label_id = 'player{}_proposal'.format(pl)
            if pl == dec_pl:
                mode_text = GAME_MODE_TEXTS[self.current_game_state['game_mode']]
                self.set_proposition_text(label_id, mode_text)
            else:
                self.remove_widget_from_display_by_id(label_id)

        # remove mode buttons
        self.remove_widget_from_display_by_id('mode_buttons')

        self.play_next_card()

    def play_next_card(self, *args):
        game = Game(players=self.playerlist, game_state=self.current_game_state)


        print(self.current_game_state)                   #############


        if not game.finished():
            curr_pl = game.get_current_player()
            if curr_pl == self.human_player_index:
                # set callbacks for legal actions
                legal_actions = game.get_possible_actions()


                print(' legal actions : ', legal_actions)   ################


                for card in legal_actions:
                    # determine which button corresponds to this card
                    for widget_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                        btn = self.ids[widget_id]
                        if btn.text == str(card):
                            break
                    assert btn
                    self.set_callback(btn=btn, callback=partial(self.choose_card, card))
            else:
                # play opponent game, update current game state
                game.next_action()
                self.current_game_state = game.get_game_state()
                # display image


                print(curr_pl)             ##########################



                widget_id = 'player{}_card'.format(curr_pl)
                if not game.trick_game.current_trick.finished():
                    card = self.current_game_state['current_trick'].cards[curr_pl]
                else:
                    card = self.current_game_state['tricks'][-1].cards[curr_pl]
                file_path = self.get_filepath(card)
                self.add_widget_to_display_by_id(widget_id)
                self.ids[widget_id].source = file_path

                if game.trick_game.current_trick.finished():
                    self.finish_trick()
                else:
                    self.play_next_card()

        else:
            self.finish_game()

    def choose_card(self, card, *args):
        # update current game state
        self.playerlist[self.human_player_index].favorite_cards = [card]
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        game.next_action()
        self.current_game_state = game.get_game_state()
        # display image
        widget_id = 'player{}_card'.format(self.human_player_index)
        file_path = self.get_filepath(card)
        self.add_widget_to_display_by_id(widget_id)
        self.ids[widget_id].source = file_path

        # remove all callbacks
        for btn in self.ids['cards'].children:
            self.clear_callbacks(btn)

        if game.trick_game.current_trick.num_cards == 0:
            self.finish_trick()
        else:



            print(' Choose card was run')     ###################



            self.play_next_card()


    def finish_trick(self):
        time.sleep(2)
        print('finish trick')
        pass

    def finish_game(self):
        # calculate and show winners, rewards etc.
        pass

    def print_msg(self, string, *args):
        print(string)



class CardWidgetTrickplay(FloatLayout):
    def do_layout(self, *args):
        width = int(self.width * 0.6)
        height = int(self.height * 0.2)
        width_per_child = int(width // 8)
        start_x = int(0.2 * self.width)
        x_positions = range(start_x, start_x + 8 * width_per_child, width_per_child)
        y_position = self.height * 0.01
        for position, child in zip(x_positions, self.children):
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
