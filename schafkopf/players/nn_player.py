import keras
import numpy as np

import schafkopf.players.data.encodings as enc
from schafkopf.game_modes import GAME_MODES, PARTNER_MODE, SOLO, WENZ
from schafkopf.players.data.data_processing import switch_suits_played_cards, switch_card_suit
from schafkopf.players.player import Player
from schafkopf.suits import ACORNS, HEARTS


class NNPlayer(Player):
    def __init__(self, game_mode_nn=None, partner_nn=None, wenz_nn=None, solo_nn=None, use_extended_models=False, name='NNPlayer'):
        Player.__init__(self, name=name)
        self.use_extended_models = use_extended_models
        try:
            self.game_mode_nn = keras.models.load_model(game_mode_nn)
        except:
            self.game_mode_nn = None
        try:
            self.partner_nn = keras.models.load_model(partner_nn)
        except:
            self.partner_nn = None
        try:
            self.solo_nn = keras.models.load_model(solo_nn)
        except:
            self.solo_nn = None
        try:
            self.wenz_nn = keras.models.load_model(wenz_nn)
        except:
            self.wenz_nn = None


    def choose_game_mode(self, public_info, options):
        hand_encoded = enc.encode_one_hot_hand(self.hand)
        pred = self.game_mode_nn.predict(np.array([hand_encoded]))[0]
        # remove not possible modes
        for mode in GAME_MODES:
            if mode not in options:
                pred[GAME_MODES.index(mode)] = 0
        max_index = np.argmax(pred)
        return enc.decode_mode_index(max_index)

    def play_card(self, public_info, options):
        if len(options) == 1:
            card = options[0]
            self.hand.remove(card)
            return card
        else:
            # predict next card (with possibly switched suits)
            pred = self.make_card_prediction(public_info)

            # switch option suits accordingly
            options_switched_suits = self.switch_suits_options(options, public_info)

            # set all non legal actions from the prediction to zero

            card_deck = [(i // 4, i % 4) for i in range(32)]
            for card in card_deck:
                if card not in options_switched_suits:
                    pred[card_deck.index(card)] = 0

            max_index = np.argmax(pred)
            best_card = card_deck[max_index]

            game_suit = public_info['game_mode'][1]
            if public_info['game_mode'][0] == PARTNER_MODE:
                best_card = switch_card_suit(best_card, game_suit, ACORNS)
            elif public_info['game_mode'][0] == SOLO:
                best_card = switch_card_suit(best_card, game_suit, HEARTS)

            assert best_card in self.hand, 'Card {} not in hand: {} '.format(best_card, self.hand)

            self.hand.remove(best_card)
            return best_card

    def switch_suits_options(self, options, public_info):
        game_suit = public_info['game_mode'][1]
        if public_info['game_mode'][0] == PARTNER_MODE:
            options_switched_suits = [switch_card_suit(card, game_suit, ACORNS) for card in options]
        elif public_info['game_mode'][0] == SOLO:
            options_switched_suits = [switch_card_suit(card, game_suit, HEARTS) for card in options]
        else:
            options_switched_suits = options
        return options_switched_suits

    def make_card_prediction(self, public_info):

        card_sequence = self.create_card_sequence(public_info)
        card_seq_switched_suits = self.switch_suits(card_sequence, public_info)
        rel_pos = (public_info['current_trick'].current_player_index - public_info['declaring_player']) % 4
        card_seq_encoded = enc.encode_played_cards(card_seq_switched_suits, rel_pos)

        if not self.use_extended_models:
            x = np.array([card_seq_encoded])
        else:
            hand_encoded = enc.encode_one_hot_hand(self.starting_hand)
            x = [np.array([card_seq_encoded]), np.array([hand_encoded])]

        if public_info['game_mode'][0] == PARTNER_MODE:
            pred = self.partner_nn.predict(x)[0]
        elif public_info['game_mode'][0] == WENZ:
            pred = self.wenz_nn.predict(x)[0]
        else:
            pred = self.solo_nn.predict(x)[0]

        return pred

    def create_card_sequence(self, public_info):
        card_sequence = []
        declaring_player = public_info['declaring_player']

        for trick in public_info['tricks']:
            leading_pl = trick.leading_player_index
            for playerindex in [(leading_pl + i) % 4 for i in range(4)]:
                card_sequence.append((trick.cards[playerindex], playerindex))

        curr_pl = public_info['current_trick'].leading_player_index
        curr_card = public_info['current_trick'].cards[curr_pl]
        while curr_card is not None:
            card_sequence.append((curr_card, curr_pl))
            curr_pl = (curr_pl + 1) % 4
            curr_card = public_info['current_trick'].cards[curr_pl]

        card_sequence = [(card, (player - declaring_player) % 4) for card, player in card_sequence]
        return card_sequence

    def switch_suits(self, card_sequence, public_info):
        game_suit = public_info['game_mode'][1]
        if public_info['game_mode'][0] == PARTNER_MODE:
            card_seq_switched_suits = switch_suits_played_cards(card_sequence, game_suit, ACORNS)
        elif public_info['game_mode'][0] == SOLO:
            card_seq_switched_suits = switch_suits_played_cards(card_sequence, game_suit, HEARTS)
        else:
            card_seq_switched_suits = card_sequence
        return card_seq_switched_suits
