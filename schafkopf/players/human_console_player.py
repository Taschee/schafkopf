from schafkopf.players.player import Player


class HumanPlayer(Player):
    """Player for playing on console"""
    def choose_game_mode(self, public_info, options):
        while True:
            mode = input("Hand : {} \n"
                         "Previous Proposals: {} \n"
                         "Choose Game Mode : ".format(self.hand, public_info["mode_proposals"]))
            if mode in options:
                break
        return mode

    def play_card(self, public_info, options=None):
        while True:
            card = input("Hand : {} \n"
                         "Current Trick : {}\n"
                         "Play card : ".format(self.hand, public_info["current_trick"]))
            if card in self.hand:
                break
        self.hand.remove(card)
        return card
