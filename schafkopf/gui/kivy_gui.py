import random
from functools import partial
from pathlib import PurePath

from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.helpers import sort_hand
from schafkopf.suits import *
from schafkopf.game_modes import *
from schafkopf.players import RandomPlayer, HeuristicsPlayer, DummyPlayer, UCTPlayer

from schafkopf.gui.player_hand_widget import PlayerHandWidget
from schafkopf.gui.bid_button import BidButton
from schafkopf.gui.image_button import ImageButton
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock


SUITS = {'0': 'Schellen', '1': 'Herz', '2': 'Gras', '3': 'Eichel'}
SYMBOLS = {'0': '7', '1': '8', '2': '9', '3': 'U', '4': 'O', '5': 'K', '6': '10', '7': 'A'}
BIDDING_IDS = {(NO_GAME, None): 'no_game', (PARTNER_MODE, ACORNS): 'partner_acorns',
               (PARTNER_MODE, LEAVES): 'partner_leaves', (PARTNER_MODE, BELLS): 'partner_bells',
               (WENZ, None): 'wenz', (SOLO, ACORNS): 'solo_acorns', (SOLO, LEAVES): 'solo_leaves',
               (SOLO, HEARTS): 'solo_hearts', (SOLO, BELLS): 'solo_bells'}
GAME_MODE_TEXTS = {(NO_GAME, None): 'Weiter', (PARTNER_MODE, ACORNS): 'Mit der Alten',
                   (PARTNER_MODE, LEAVES): 'Mit der Blauen!', (PARTNER_MODE, BELLS): 'Mit der Schellen',
                   (WENZ, None): 'Wenz', (SOLO, ACORNS): 'Eichel Solo', (SOLO, LEAVES): 'Gras Solo',
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


class GameResultsScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


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

    def remove_card_from_display(self, card):
        card_str = str(card)
        player_hand_widget = self.ids['player_hand']
        for wid in player_hand_widget.children:
            if wid.text == card_str:
                player_hand_widget.remove_widget(wid)


    def add_widget_to_display_by_id(self, widget_id, *args):
        widget = self.ids[widget_id]
        if widget not in self.ids['display'].children:
            self.ids['display'].add_widget(self.ids[widget_id])

    def display_human_player_hand(self):
        hand = sort_hand(self.current_game_state['player_hands'][self.human_player_index])
        for card, widget in zip(hand, self.ids['player_hand'].children):
            filepath = self.get_filepath(card)
            widget.source = filepath
            widget.text = str(card)

    def remove_current_trick_from_display(self):
        for pl in range(4):
            widget_id = 'player{}_card'.format(pl)
            self.remove_widget_from_display_by_id(widget_id)

    def get_filepath(self, card):
        im_name = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
        filepath = PurePath('..', 'images', im_name)
        return str(filepath)

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
        self.remove_widget_from_display_by_id('next_trick_button')
        self.start_bidding()

    def start_bidding(self):
        curr_pl = self.current_game_state['current_player_index']
        while curr_pl != self.human_player_index:
            self.make_first_opponent_proposal(curr_pl)
            curr_pl = self.current_game_state['current_player_index']
        # set callbacks for legal actions
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        legal_actions = game.get_possible_actions()
        for action in legal_actions:
            action_id = BIDDING_IDS[action]
            btn = self.ids[action_id]
            self.set_callback(btn=btn, callback=partial(self.make_first_proposal, action))

    def make_first_opponent_proposal(self, curr_pl, *args):
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
        while len(self.current_game_state['mode_proposals']) < 4:
            curr_pl = self.current_game_state['current_player_index']
            self.make_first_opponent_proposal(curr_pl)
        game = Game(players=playerlist, game_state=self.current_game_state)
        if game.bidding_game.finished():
            self.prepare_trick_play()
        else:
            self.continue_bidding()

    def continue_bidding(self, *args):
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

    def prepare_trick_play(self, *args):
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

        if not game.finished():
            curr_pl = game.get_current_player()

            if curr_pl == self.human_player_index:
                # set callbacks for legal actions
                legal_actions = game.get_possible_actions()

                for card in legal_actions:
                    # determine which button corresponds to this card
                    widget_ids = ['card_{}'.format(i) for i in range(1, 9)]
                    for widget_id in widget_ids:
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

                widget_id = 'player{}_card'.format(curr_pl)

                if game.trick_game.current_trick.num_cards != 0:
                    card = self.current_game_state['current_trick'].cards[curr_pl]
                else:
                    card = self.current_game_state['tricks'][-1].cards[curr_pl]

                file_path = self.get_filepath(card)
                self.add_widget_to_display_by_id(widget_id)
                self.ids[widget_id].source = file_path

                if game.trick_game.current_trick.num_cards == 0:
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
        for btn in self.ids['player_hand'].children:
            self.clear_callbacks(btn)

        # remove played card widget
        self.remove_card_from_display(card)

        if game.trick_game.current_trick.num_cards == 0:
            self.finish_trick()
        else:
            self.play_next_card()

    def finish_trick(self, *args):
        self.add_widget_to_display_by_id('next_trick_button')

    def next_trick(self, *args):
        # remove current trick widgets
        self.remove_widget_from_display_by_id('next_trick_button')
        self.remove_current_trick_from_display()
        self.play_next_card()

    def finish_game(self, *args):
        # calculate winners, rewards etc.
        game = Game(players=self.playerlist, game_state=self.current_game_state)
        game_mode = self.current_game_state['game_mode']
        if game_mode[0] != NO_GAME:
            game_mode_str = GAME_MODE_TEXTS[game_mode]
            final_score = game.score_offensive_players()
            rewards = game.get_payouts()
            winners = game.determine_winners()
            # display results on result screen
            result_screen = self.manager.get_screen('result_screen')
            if final_score > 60:
                result_screen.ids['winners'].text = '{} gewonnen von {} mit {} Punkten'.format(game_mode_str,
                                                                                               winners,
                                                                                               final_score)
            else:
                result_screen.ids['winners'].text = '{} gewonnen von {} mit {} Punkten'.format(game_mode_str,
                                                                                               winners,
                                                                                               final_score)
            result_screen.ids['rewards'].text = 'Auszahlung : '+format(rewards)
            self.manager.current = 'result_screen'
        else:
            game_mode_str = GAME_MODE_TEXTS[game_mode]
            rewards = game.get_payouts()
            # display results on result screen
            result_screen = self.manager.get_screen('result_screen')
            result_screen.ids['winners'].text = 'Zamgschmissen'
            result_screen.ids['rewards'].text = 'Auszahlung : ' + format(rewards)
            self.manager.current = 'result_screen'


    def print_msg(self, string, *args):
        print(string)


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
