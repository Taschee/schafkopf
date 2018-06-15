from twocardgame.cfr_trainer import NodeMap, Node, CFRTrainer
from twocardgame.players import CFRPlayer, RandomPlayer
from twocardgame.twocardgame import TwoCardGame,ThreePlayerTrick
import twocardgame.cfr_again as cfr


player0 = CFRPlayer(name="Player 0") ####### rüber in CFR?
player1 = CFRPlayer(name="Player 1")
player2 = CFRPlayer(name="Player 2")
cfr_trainer = CFRTrainer(playerlist=[player0, player1, player2])
cfr_trainer.train(iterations=1)

