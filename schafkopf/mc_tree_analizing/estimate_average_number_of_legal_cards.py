#!/usr/bin/env python3
import random

from schafkopf.tournaments.game_states_trick_play import sample_game_states
from schafkopf.game import Game
from schafkopf.players import RandomPlayer


def main():
    num_examples = 0
    num_poss = 0
    for i in range(10):
        for state in sample_game_states:
            playerlist = [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]
            game = Game(players=playerlist,
                        game_state=state)

            while not game.finished():
                if len(game.trick_game.tricks) < 7:

                    if game.trick_game.current_trick.num_cards != 0:
                        current_player = game.trick_game.get_current_player()
                        options = game.trick_game.possible_cards(game.trick_game.current_trick, current_player.get_hand())
                        num_poss += len(options)
                        num_examples += 1

                game.trick_game.play_next_card()
                game.trick_game.trick_finished()

    print('Average number of legal cards to play after {} situations is : {}'.format(num_examples, num_poss / num_examples))

if __name__ == '__main__':
    main()
