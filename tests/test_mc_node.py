import pytest

from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.players.mc_node import MCNode
from schafkopf.suits import SUITS, LEAVES


@pytest.fixture
def next_state(player_hands_partner):
    leading_player = 0
    current_player = 1
    mode_proposals = [(NO_GAME, None)]
    game_mode = (NO_GAME, None)
    offensive_players = []
    tricks = []
    current_trick = None
    possible_actions = [(NO_GAME, None), (WENZ, None)] + [(PARTNER_MODE, suit) for suit in SUITS]\
                                                       + [(SOLO, suit) for suit in SUITS]
    return {"player_hands": player_hands_partner,
            "possible_actions": possible_actions,
            "current_player_index": current_player,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}

@pytest.fixture
def different_next_state(player_hands_partner):
    leading_player = 0
    current_player = 1
    mode_proposals = [(PARTNER_MODE, LEAVES)]
    game_mode = (PARTNER_MODE, LEAVES)
    offensive_players = []
    tricks = []
    current_trick = None
    possible_actions = [(WENZ, None)] + [(SOLO, suit) for suit in SUITS]
    return {"player_hands": player_hands_partner,
            "possible_actions": possible_actions,
            "current_player_index": current_player,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}


def test_add_node(game_state_partner, next_state, different_next_state):
    root_node = MCNode(game_state=game_state_partner, parent=None, previous_action= None)
    child = MCNode(game_state=next_state, parent=root_node, previous_action=(NO_GAME, None))
    root_node.add_child(child)
    assert len(root_node.children) == 1
    child.update_rewards([30, 30, -30, -30])
    child.update_visits()
    root_node.update_visits()
    assert child.current_player == 1
    assert child.get_average_reward(child.current_player) == 30
    child.update_rewards([20, 20, -20, -20])
    child.update_visits()
    root_node.update_visits()
    assert child.get_average_reward(child.current_player) == 25
    sec_child = MCNode(game_state=different_next_state, parent=root_node, previous_action=(PARTNER_MODE, LEAVES))
    assert not root_node.fully_expanded()
    sec_child.update_rewards([-20, 20, 20, -20])
    sec_child.update_visits()
    root_node.update_visits()
    assert root_node.best_child(ucb_const=1).previous_action == (NO_GAME, None)

