

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

    def visualize(self):
        # create some visualization of the tree?
        pass
