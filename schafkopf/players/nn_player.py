import keras
import numpy as np
from schafkopf.players.player import Player
import schafkopf.players.data.encodings as enc
from schafkopf.game_modes import GAME_MODES, PARTNER_MODE, SOLO, WENZ
from schafkopf.suits import ACORNS, HEARTS


class NNPlayer(Player):
    def __init__(self, game_mode_nn, partner_nn, wenz_nn, solo_nn, name='NNPlayer'):
        Player.__init__(self, name=name)
        self.game_mode_nn = keras.models.load_model(game_mode_nn)
        self.partner_nn = keras.models.load_model(partner_nn)
        self.solo_nn = keras.models.load_model(solo_nn)
        self.wenz_nn = keras.models.load_model(wenz_nn)

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
        card_sequence = self.create_card_sequence(public_info)

        if public_info['game_mode'][0] == PARTNER_MODE:
            card_seq_switched_suits = self.switch_suit(public_info['game_mode'][1], ACORNS)
            card_seq_encoded = self.encode_seq(card_seq_switched_suits)
            pred = self.partner_nn.predict(np.array(card_seq_encoded))[0]
        elif public_info['game_mode'][0] == WENZ:
            card_seq_encoded = self.encode_seq(card_sequence)
            pred = self.wenz_nn.predict(np.array(card_seq_encoded))[0]
        else:
            card_seq_switched_suits = self.switch_suit(public_info['game_mode'][1], HEARTS)
            card_seq_encoded = self.encode_seq(card_seq_switched_suits)
            pred = self.solo_nn.predict(np.array(card_seq_encoded))[0]

        card_deck = [(i // 4, i % 4) for i in range(32)]
        for card in card_deck:
            if card not in options:
                pred[card_deck.index(card)] = 0

        max_index = np.argmax(pred)
        return card_deck[max_index]

    def create_card_sequence(self, public_info):
        # should switch suits
        pass

    def switch_suit(self, param, ACORNS):
        pass

    def encode_seq(self, card_seq_switched_suits):
        pass





