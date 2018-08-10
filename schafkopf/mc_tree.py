import graphviz
from schafkopf.suits import SUITS, ACORNS, LEAVES, HEARTS, BELLS
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE

import random


class MCTree:
    def __init__(self, root_node):
        self.root_node = root_node
        self.nodes = {root_node}

    def add_node(self, node, parent_node):
        self.nodes.add(node)
        parent_node.add_child(node)

    def backup_rewards(self, leaf_node, rewards):
        current_node = leaf_node
        while current_node != self.root_node:
            current_node.update_rewards(rewards)
            current_node.update_visits()
            current_node = current_node.parent
        self.root_node.update_visits()

    def get_depth(self, node):
        current_node = node
        depth = 0
        while current_node != self.root_node:
            depth += 1
            current_node = current_node.parent
        return depth

    def get_leaves(self):
        leaves = set()
        for node in self.nodes:
            if node.is_leaf():
                leaves.add(node)
        return leaves

    def max_depth(self):
        max_depth = 0
        for node in self.get_leaves():
            depth = self.get_depth(node)
            if depth > max_depth:
                max_depth = depth
        return max_depth

    def average_depth(self):
        all_depths = [leave.get_depth() for leave in self.get_leaves()]
        return sum(all_depths) / len(all_depths)

    def visualize_tree(self, format="png", ucb=None):
        """Create a visualization of the tree and save it as .png as well as .gv"""
        graph = graphviz.Digraph(filename="Tree_{}nodes{}.gv".format(len(self.nodes) - 1, ucb),
                                 format=format,
                                 node_attr={"shape": "ellipse", "fixedsize": "True"})
        self.add_tree(graph=graph,
                      my_root_node=self.root_node)
        graph.render()

    def add_tree(self, graph, my_root_node, graph_root_name=None):
        # recursively add nodes and draw all edges
        if graph_root_name is None:
            graph.node(name="ROOT", label="", **{'width':str(0), 'height':str(0)})
            graph_root_name = "ROOT"
        for child in my_root_node.children:
            new_name = str(random.choice(range(10**10)))
            img = self.get_image_name(card=child.previous_action)
            graph.node(name=new_name, image=img, label="", **{'width':str(0.5), 'height':str(0.3)})
            graph.edge(graph_root_name, new_name)
            self.add_tree(graph=graph, my_root_node=child, graph_root_name=new_name)

    def get_image_name(self, card):
        img = "../images/"
        if card[1] == BELLS:
            img += "Schellen"
        elif card[1] == HEARTS:
            img += "Herz"
        elif card[1] == LEAVES:
            img += "Gras"
        else:
            img += "Eichel"
        if card[0] in {SEVEN, EIGHT, NINE}:
            img += str(card[0] + 7)
        elif card[0] == TEN:
            img += str(10)
        elif card[0] == UNTER:
            img += "U"
        elif card[0] == OBER:
            img += "O"
        elif card[0] == KING:
            img += "K"
        else:
            img += "A"
        img += ".jpg"
        return img
