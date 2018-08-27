import time
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.players.heuristics_player import HeuristicsPlayer
from schafkopf.tournament import Tournament




def main():
    playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=0.1),
                  HeuristicsPlayer(name="B"), HeuristicsPlayer(name="C"), HeuristicsPlayer(name="D")]

    tournament = Tournament(playerlist, number_of_games=10)

    start_time = time.time()
    tournament.play()
    end_time = time.time()

    print("Time : ", end_time - start_time, " seconds")
    print("Results : ", tournament.get_tournament_results())


if __name__ == "__main__":
    main()
