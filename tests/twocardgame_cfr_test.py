from twocardgame.cfr_again import Node, NodeMap, CFRTrainer, History
import random

cfr_trainer = CFRTrainer()

cards = [(3, 0), (2, 0), (1, 0), (3, 1), (2, 1), (1, 1)]

history = History(mode_proposals=[], cards_played=[], starting_deck=cards)

cfr_trainer.train(10000)
