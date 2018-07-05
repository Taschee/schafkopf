from twocardgame.cfr import CFRTrainer


cfr_trainer = CFRTrainer()

cfr_trainer.train(10)

all_nodes = cfr_trainer.node_map.get_nodes()

for node in all_nodes:
    print("Node : ", node.infoset)
    print("Strategy : ",node.get_average_strategy())
