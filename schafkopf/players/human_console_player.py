from schafkopf.players.player import Player


class HumanConsolePlayer(Player):
    """Player for playing on console"""
    def choose_game_mode(self, public_info, options):
        options = list(options)
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
                         "Game Mode : {}"
                         "Previous tricks : {}\n"
                         "Current Trick : {}\n"
                         "Options : {}\n" 
                         "Play card : ".format(self.hand,
                                               public_info['game_mode'],
                                               [str(trick) for trick in public_info['tricks']],
                                               public_info["current_trick"],
                                               options))
            card_index = int(card_index)
            if card_index in range(len(options)):
                break
        card = options[card_index]
        self.hand.remove(card)
        return card
