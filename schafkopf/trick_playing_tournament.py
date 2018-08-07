from schafkopf.game import Game
from schafkopf.players import RandomPlayer
from schafkopf.uct_player import UCTPlayer
import time
from schafkopf.game_states_trick_play import sample_game_states


playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=10),
              RandomPlayer(name="B"),
              RandomPlayer(name="C"),
              RandomPlayer(name="D")]

def main():
    all_rewards = []
    total_scores = [0, 0, 0, 0]

    for num in range(len(sample_game_states)):
        start_time = time.time()
        game_state = sample_game_states[num]
        game = Game(game_state=game_state, players=playerlist)
        game.play()
        rewards = game.get_payouts()
        all_rewards.append(rewards)
        for i in range(4):
            total_scores[i] += rewards[i]
        end_time = time.time()
        print("Game {} took {} seconds".format(num + 1, end_time - start_time))
        print("Rewards : ", rewards)

    print("Final scores : ", total_scores)


if __name__ == "__main__":
    main()
