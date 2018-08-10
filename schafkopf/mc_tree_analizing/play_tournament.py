import time
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.tournament import Tournament


playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=1),
              RandomPlayer(), RandomPlayer(), RandomPlayer()]


def main():
    playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100),
                  RandomPlayer(name="B"), RandomPlayer(name="C"), RandomPlayer(name="D")]

    tournament = Tournament(playerlist, number_of_games=10)

    start_time = time.time()
    tournament.play()
    end_time = time.time()

    print("Time : ", end_time - start_time, " seconds")
    print("Results : ", tournament.get_tournament_results())


if __name__ == "__main__":
    main()
