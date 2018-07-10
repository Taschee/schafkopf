from schafkopf.game import Game
from schafkopf.players import RandomPlayer

Alfons = RandomPlayer(name="Alfons")
Bertl = RandomPlayer(name="Bertha")
Chrissie = RandomPlayer(name="Chris")
Dora = RandomPlayer(name="Dora")

playerlist = [Alfons, Bertl, Chrissie, Dora]
game = Game(playerlist)

game.decide_game_mode()