from copy import deepcopy
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.ranks import ACE
from schafkopf.helpers import define_trumpcards
from schafkopf.trick import Trick


class TrickGame:
    def __init__(self, playerlist, game_state):
        self.playerlist = playerlist
        self.max_num_tricks = 8
        self.leading_player_index = game_state['leading_player_index']
        self.game_mode = game_state['game_mode']
        self.mode_proposals = game_state['mode_proposals']
        self.offensive_players = [game_state['declaring_player']]
        if self.game_mode[0] == PARTNER_MODE:
            for player in self.playerlist:
                if (7, self.game_mode[1]) in player.starting_hand:
                    self.offensive_players.append(self.playerlist.index(player))
                    break
        self.trumpcards = define_trumpcards(self.game_mode)
        self.tricks = game_state['tricks']
        if game_state['current_trick'] is not None:
            self.current_trick = game_state['current_trick']
        else:
            self.current_trick = Trick(leading_player_index=self.leading_player_index)
        self.current_player_index = self.current_trick.current_player_index
        self.scores = [0 for player in playerlist]
        for trick in game_state["tricks"]:
            self.scores[trick.winner] += trick.calculate_points()

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % 4
        self.current_trick.current_player_index = self.current_player_index

    def get_current_player(self):
        return self.playerlist[self.current_player_index]

    def get_public_info(self):
        mode_proposals_public = []
        for proposal in self.mode_proposals:
            if proposal[0] == NO_GAME:
                mode_proposals_public.append(0)
            else:
                mode_proposals_public.append(1)
        return deepcopy({'leading_player_index': self.leading_player_index,
                         'current_player_index': self.current_player_index,
                         'mode_proposals': mode_proposals_public,
                         'declaring_player': self.offensive_players[0],
                         'game_mode': self.game_mode,
                         'trumpcards': self.trumpcards,
                         'tricks': self.tricks,
                         'current_trick': self.current_trick})

    def suit_in_hand(self, suit, hand):
        suit_cards = [card for card in hand if card[1] == suit and card not in self.trumpcards]
        if len(suit_cards) > 0:
            return suit_cards
        else:
            return hand

    def possible_cards(self, current_trick, hand):

        if current_trick.num_cards == 0:
            # " Check in case of PARTNER MODE if running away is possible"
            if self.game_mode[0] == PARTNER_MODE and (ACE, self.game_mode[1]) in hand:
                if len(self.suit_in_hand(suit=self.game_mode[1], hand=hand)) < 4:
                    forbidden_cards = [card for card in hand if card not in self.trumpcards
                                       and card[1] == self.game_mode[1] and card[0] != 7]
                    poss_cards = [card for card in hand if card not in forbidden_cards]
                else:
                    poss_cards = hand
            else:
                poss_cards = hand

        else:
            first_card = current_trick.cards[current_trick.leading_player_index]

            if first_card in self.trumpcards:
                players_trumpcards = [trump for trump in self.trumpcards if trump in hand]
                if len(players_trumpcards) > 0:
                    poss_cards = players_trumpcards
                else:
                    poss_cards = hand
            elif self.game_mode[0] == PARTNER_MODE and first_card[1] == self.game_mode[1] \
                    and (7, self.game_mode[1]) in hand:
                previously_ran_away = self.previously_ran_away()
                if not previously_ran_away:
                    poss_cards = [(7, self.game_mode[1])]
                else:
                    suit = first_card[1]
                    poss_cards = self.suit_in_hand(suit, hand)
            else:
                suit = first_card[1]
                poss_cards = self.suit_in_hand(suit, hand)

            # check if searched Ace can be played
            poss_cards = poss_cards[:]
            if self.game_mode[0] == PARTNER_MODE and (ACE, self.game_mode[1]) in poss_cards:
                if not self.previously_ran_away() and len(poss_cards) > 1:
                    poss_cards.remove((ACE, self.game_mode[1]))

        return poss_cards[:]

    def reset_current_trick(self):
        self.tricks.append(self.current_trick)
        self.current_trick = Trick(self.current_player_index)

    def play_next_card(self):
        current_player = self.get_current_player()
        if self.current_trick.num_cards == 0:
            self.current_trick.leading_player_index = self.current_player_index
        options = self.possible_cards(self.current_trick, current_player.get_hand())
        info = self.get_public_info()
        next_card = current_player.play_card(public_info=info, options=options)
        assert next_card in options, 'Player {} tried to play non legal card'.format(current_player)
        self.current_trick.cards[self.current_player_index] = next_card
        self.current_trick.num_cards += 1

    def trick_finished(self):
        if self.current_trick.finished():
            self.current_trick.calculate_points()
            self.current_trick.determine_trickwinner(self.trumpcards)
            self.current_player_index = self.current_trick.winner
            self.scores[self.current_player_index] += self.current_trick.score
            self.reset_current_trick()
        else:
            self.next_player()

    def finished(self):
        if len(self.tricks) == self.max_num_tricks or self.game_mode[0] == NO_GAME:
            return True
        else:
            return False

    def play(self):
        while not self.finished():
            self.play_next_card()
            self.trick_finished()

    def previously_ran_away(self):
        prev_ran_away = False
        partnerindex = self.offensive_players[1]
        searched_suit = self.game_mode[1]
        for trick in self.tricks:
            if trick.leading_player_index == partnerindex and trick.cards[partnerindex][0] == searched_suit:
                prev_ran_away = True
                break
        return prev_ran_away
