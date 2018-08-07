import numpy as np


class MCNode:
    def __init__(self, game_state, parent=None, previous_action=None):
        self.children = []
        self.parent = parent
        self.game_state = game_state
        self.current_player = game_state["current_player_index"]
        self.previous_action = previous_action
        self.visits = 0
        self.cumulative_rewards = [0 for i in range(4)]

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def is_terminal(self):
        if len(self.game_state["tricks"]) == 8:
            return True
        else:
            return False

    def fully_expanded(self):
        if len(self.children) == len(self.game_state["possible_actions"]):
            return True
        else:
            return False

    def best_child(self, ucb_const):
        if not self.is_leaf():
            values = [child.ucb_value(ucb_const) for child in self.children]
            best_child = self.children[np.argmax(values)]
            return best_child

    def ucb_value(self, ucb_const):
        if self.visits != 0:
            average_reward = self.get_average_reward(player=self.parent.current_player)
            return average_reward + ucb_const * np.sqrt(2 * np.log(self.parent.visits) / self.visits)
        else:
            return np.infty

    def ucb_values(self, ucb_const):
        return [child.ucb_value(ucb_const) for child in self.children]

    def update_visits(self):
        self.visits += 1

    def update_rewards(self, rewards):
        for i in range(len(self.cumulative_rewards)):
            self.cumulative_rewards[i] += rewards[i]

    def get_average_reward(self, player):
        if self.visits > 0:
            return self.cumulative_rewards[player] / self.visits
        else:
            return 0
