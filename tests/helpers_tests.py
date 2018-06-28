from schafkopf.game import Game
from schafkopf.players import RandomPlayer
import schafkopf.helpers as hlp


Alfons = RandomPlayer(name="Alfons")
Bertl = RandomPlayer(name="Bertha")
Chrissie = RandomPlayer(name="Chris")
Dora = RandomPlayer(name="Dora")

playerlist = [Alfons, Bertl, Chrissie, Dora]

testgame = Game(players=playerlist)

testgame.decide_game_mode()

print("Game mode : ", testgame.get_game_mode())
print("Offensive players : ", testgame.get_offensive_players())
print("Alfons cards : ", Alfons.get_hand())
print("Possible opponent hands : ", hlp.sample_opponent_cards(testgame, Alfons))

for i in range(24):
    testgame.play_next_card()
    testgame.trick_finished()
for trick in testgame.get_tricks():
    print(trick)
    print("Winner : ", trick.winner)


print("Alfons cards : ", Alfons.get_hand())
print("Possible opponent hands : ", hlp.sample_opponent_cards(testgame, Alfons))