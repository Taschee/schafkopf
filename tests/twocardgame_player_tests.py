from twocardgame.twocardgame import TwoCardGame
from twocardgame.players import CFRPlayer, RandomPlayer


Adi = CFRPlayer(name="Adi")
Bepp = CFRPlayer(name="Bepp")
Carl = CFRPlayer(name="Carl")
playerlist = [Adi, Bepp, Carl]

game = TwoCardGame(playerlist)


