from schafkopf.players.player import Player


class HumanConsolePlayer(Player):
    """Player for playing on console"""
    def choose_game_mode(self, public_info, options):
        while True:
            mode_index = input("Hand : {} \n"
                         "Previous Proposals: {} \n"
                         "Options : {}\n"
                         "Choose Game Mode : ".format(self.hand, public_info["mode_proposals"], options))
            mode = options[int(mode_index)]
            if mode in options:
                break
        return mode

    def play_card(self, public_info, options=None):
        while True:
            card_index = input("Hand : {} \n"
                         "Previous tricks : {}"
                         "Current Trick : {}\n"
                         "Options : {}\n" 
                         "Play card : ".format(self.hand, public_info['tricks'], public_info["current_trick"], options))
            card = options[int(card_index)]
            if card in self.hand:
                break
        self.hand.remove(card)
        return card
