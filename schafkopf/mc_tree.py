

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
