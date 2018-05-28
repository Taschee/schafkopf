from schafkopf.twocardgame import TwoCardGame
from schafkopf.players import RandomPlayer

Alfons = RandomPlayer(name="Alfons")
Bertl = RandomPlayer(name="Bertha")
Chrissie = RandomPlayer(name="Chris")

playerlist = [Alfons, Bertl, Chrissie]

testgame = TwoCardGame(players=playerlist, leading_player_index=0)

testgame.decide_game_mode()

print("offensive player : ", testgame._offensive_players)
print("game mode :    ",testgame.get_game_mode())
print("trumpcards :  ",  testgame._trump_cards)

while not testgame.finished():
    testgame.play_next_card()
    print("current player :    ", testgame.get_current_playerindex())
    print("current trick  :    ", testgame.get_current_trick().cards)
    print("Tricks :     " , testgame.get_tricks())
    testgame.trick_finished()

print("Tricks : ", testgame.get_tricks())
print("Winners : ", testgame.determine_winners())
