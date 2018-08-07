from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.suits import ACORNS, BELLS, HEARTS, LEAVES


def define_game_state(player_hands, leading_player_index, mode_proposals):
    return {"player_hands": player_hands,
            "leading_player_index": leading_player_index,
            "current_player_index": leading_player_index,
            "declaring_player": 0,
            "game_mode": mode_proposals[0],
            "mode_proposals": mode_proposals,
            "tricks": [],
            "current_trick": None,
            "possible_actions": player_hands[leading_player_index]}

partner_hands_1 = [[(3, 1), (4, 1), (3, 3), (6, 0), (6, 2), (6, 1), (3, 0), (0, 2)],
                   [(2, 3), (4, 3), (1, 1), (5, 1), (7, 3), (5, 3), (5, 0), (6, 3)],
                   [(2, 1), (7, 0), (1, 3), (0, 1), (4, 0), (2, 0), (5, 2), (0, 0)],
                   [(1, 2), (3, 2), (7, 1), (0, 3), (2, 2), (1, 0), (7, 2), (4, 2)]]
partner_proposals_1 = [(1, 0), (0, None), (0, None), (0, None)]

partner_hands_2 = [[(0, 1), (6, 0), (7, 3), (4, 1), (6, 1), (3, 0), (0, 2), (3, 1)],
                   [(6, 3), (7, 0), (5, 0), (2, 1), (4, 3), (7, 2), (1, 1), (1, 0)],
                   [(0, 3), (1, 2), (1, 3), (3, 2), (4, 2), (6, 2), (2, 3), (2, 0)],
                   [(0, 0), (5, 2), (2, 2), (3, 3), (5, 3), (5, 1), (7, 1), (4, 0)]]
partner_proposals_2 = [(1, 0), (0, None), (0, None), (0, None)]

partner_hands_3 = [[(0, 2), (4, 3), (5, 0), (3, 0), (5, 1), (6, 1), (7, 2), (6, 0)],
                   [(3, 1), (1, 1), (4, 1), (4, 2), (2, 3), (0, 0), (7, 3), (4, 0)],
                   [(0, 1), (5, 3), (2, 2), (5, 2), (0, 3), (6, 3), (7, 0), (2, 0)],
                   [(7, 1), (2, 1), (3, 2), (1, 0), (1, 2), (3, 3), (1, 3), (6, 2)]]
partner_proposals_3 = [(1, 0), (0, None), (0, None), (0, None)]

partner_hands_4 = [[(6, 2), (1, 2), (6, 3), (2, 1), (5, 1), (4, 3), (3, 1), (3, 3)],
                   [(0, 3), (4, 0), (7, 1), (6, 0), (2, 3), (5, 2), (7, 2), (2, 0)],
                   [(1, 1), (0, 2), (7, 3), (1, 3), (5, 0), (0, 1), (4, 2), (7, 0)],
                   [(4, 1), (5, 3), (6, 1), (2, 2), (3, 2), (1, 0), (3, 0), (0, 0)]]
partner_proposals_4 = [(1, 3), (0, None), (0, None), (0, None)]

partner_hands_5 = [[(4, 3), (4, 0), (4, 1), (7, 2), (1, 0), (0, 2), (5, 1), (2, 2)],
                   [(3, 2), (7, 3), (2, 0), (7, 1), (2, 1), (0, 0), (3, 0), (5, 2)],
                   [(5, 0), (1, 3), (6, 3), (6, 1), (5, 3), (3, 3), (7, 0), (0, 3)],
                   [(6, 0), (1, 1), (0, 1), (3, 1), (1, 2), (4, 2), (2, 3), (6, 2)]]
partner_proposals_5 = [(1, 0), (0, None), (0, None), (0, None)]

partner_hands_6 = [[(5, 1), (1, 1), (3, 1), (2, 3), (4, 3), (0, 2), (7, 2), (0, 3)],
                   [(1, 0), (3, 2), (6, 0), (5, 3), (4, 2), (6, 3), (2, 2), (7, 3)],
                   [(7, 0), (1, 3), (4, 0), (1, 2), (2, 1), (7, 1), (5, 2), (0, 1)],
                   [(6, 2), (2, 0), (3, 0), (6, 1), (5, 0), (0, 0), (3, 3), (4, 1)]]
partner_proposals_6 = [(1, 3), (0, None), (0, None), (0, None)]

partner_hands_7 = [[(4, 3), (4, 2), (2, 3), (5, 2), (1, 1), (0, 1), (3, 1), (5, 0)],
                   [(7, 2), (0, 0), (4, 1), (6, 1), (6, 0), (3, 2), (6, 2), (7, 3)],
                   [(1, 0), (3, 3), (3, 0), (7, 1), (1, 3), (7, 0), (6, 3), (0, 2)],
                   [(4, 0), (5, 3), (2, 2), (1, 2), (0, 3), (2, 1), (2, 0), (5, 1)]]
partner_proposals_7 = [(1, 2), (0, None), (0, None), (0, None)]

partner_hands_8 = [[(6, 2), (6, 1), (0, 2), (4, 0), (4, 1), (4, 2), (5, 3), (3, 2)],
                   [(3, 1), (5, 1), (1, 0), (7, 0), (2, 1), (3, 0), (7, 1), (6, 0)],
                   [(7, 2), (2, 2), (0, 0), (7, 3), (1, 3), (1, 1), (1, 2), (2, 3)],
                   [(4, 3), (0, 3), (3, 3), (5, 0), (2, 0), (5, 2), (0, 1), (6, 3)]]
partner_proposals_8 = [(1, 3), (0, None), (0, None), (0, None)]

partner_hands_9 = [[(3, 1), (5, 0), (4, 1), (7, 1), (7, 2), (2, 0), (0, 1), (4, 3)],
                   [(1, 0), (0, 2), (4, 2), (6, 0), (5, 1), (6, 2), (2, 1), (6, 1)],
                   [(1, 1), (4, 0), (1, 3), (5, 2), (0, 0), (0, 3), (3, 2), (5, 3)],
                   [(7, 0), (6, 3), (1, 2), (2, 3), (7, 3), (3, 0), (3, 3), (2, 2)]]
partner_proposals_9 = [(1, 0), (0, None), (0, None), (0, None)]

partner_hands_10 = [[(3, 1), (5, 0), (4, 2), (3, 3), (4, 3), (2, 0), (1, 3), (0, 3)],
                    [(6, 0), (1, 0), (7, 0), (5, 2), (2, 1), (0, 2), (1, 2), (0, 0)],
                    [(7, 1), (2, 3), (5, 3), (7, 2), (4, 0), (5, 1), (2, 2), (4, 1)],
                    [(7, 3), (3, 2), (6, 1), (3, 0), (6, 3), (6, 2), (0, 1), (1, 1)]]
partner_proposals_10 = [(1, 3), (0, None), (0, None), (0, None)]

solo_hands_1 = [[(1, 3), (7, 2), (4, 3), (4, 2), (3, 2), (5, 2), (3, 3), (2, 3)],
                [(7, 1), (0, 1), (6, 1), (6, 0), (0, 0), (7, 3), (0, 3), (2, 1)],
                [(7, 0), (2, 2), (6, 2), (1, 2), (3, 1), (1, 0), (4, 1), (3, 0)],
                [(5, 3), (2, 0), (0, 2), (6, 3), (5, 0), (5, 1), (1, 1), (4, 0)]]
solo_proposals_1 = [(3, 3), (0, None), (0, None), (0, None)]

solo_hands_2 = [[(1, 1), (1, 0), (4, 3), (0, 0), (4, 1), (4, 2), (6, 0), (3, 0)],
                [(4, 0), (2, 3), (7, 1), (3, 2), (2, 1), (7, 2), (5, 0), (6, 2)],
                [(2, 2), (7, 3), (0, 2), (3, 3), (3, 1), (6, 3), (6, 1), (0, 1)],
                [(2, 0), (1, 3), (1, 2), (5, 2), (5, 1), (0, 3), (5, 3), (7, 0)]]
solo_proposals_2 = [(3, 0), (0, None), (0, None), (0, None)]


solo_hands_3 = [[(2, 3), (4, 1), (3, 0), (3, 2), (4, 3), (7, 1), (4, 0), (0, 3)],
                [(7, 2), (2, 0), (6, 1), (6, 3), (4, 2), (3, 1), (0, 2), (3, 3)],
                [(2, 1), (5, 0), (0, 0), (5, 2), (7, 0), (1, 3), (6, 2), (1, 0)],
                [(2, 2), (5, 3), (7, 3), (1, 1), (0, 1), (6, 0), (5, 1), (1, 2)]]
solo_proposals_3 = [(3, 3), (0, None), (0, None), (0, None)]

solo_hands_4 = [[(4, 1), (3, 3), (7, 1), (3, 0), (0, 2), (4, 0), (7, 3), (6, 2)],
                [(5, 0), (7, 2), (0, 3), (2, 2), (3, 2), (2, 0), (6, 3), (0, 0)],
                [(5, 3), (1, 0), (1, 3), (1, 2), (6, 1), (4, 3), (4, 2), (7, 0)],
                [(1, 1), (6, 0), (2, 1), (3, 1), (0, 1), (5, 1), (2, 3), (5, 2)]]
solo_proposals_4 = [(3, 2), (0, None), (0, None), (0, None)]

solo_hands_5 = [[(6, 0), (3, 3), (4, 3), (1, 0), (0, 2), (7, 0), (7, 1), (4, 0)],
                [(4, 2), (3, 1), (5, 2), (1, 1), (0, 3), (5, 1), (0, 1), (7, 3)],
                [(3, 0), (6, 3), (5, 3), (5, 0), (2, 2), (2, 0), (4, 1), (2, 3)],
                [(0, 0), (2, 1), (1, 2), (1, 3), (6, 1), (3, 2), (6, 2), (7, 2)]]
solo_proposals_5 = [(3, 0), (0, None), (0, None), (0, None)]


wenz_hands_1 = [[(3, 0), (7, 2), (7, 3), (4, 0), (7, 0), (5, 1), (3, 3), (3, 1)],
               [(1, 2), (0, 0), (4, 2), (3, 2), (6, 2), (5, 0), (4, 1), (6, 1)],
               [(2, 1), (6, 0), (4, 3), (6, 3), (5, 2), (2, 3), (2, 2), (2, 0)],
               [(1, 0), (5, 3), (7, 1), (1, 3), (0, 1), (1, 1), (0, 3), (0, 2)]]

wenz_hands_2 = [[(3, 3), (5, 1), (4, 1), (6, 3), (6, 1), (3, 2), (2, 1), (7, 0)],
               [(4, 0), (6, 0), (7, 3), (5, 2), (2, 2), (0, 0), (1, 3), (2, 0)],
               [(1, 0), (0, 1), (4, 2), (5, 3), (0, 2), (0, 3), (7, 1), (5, 0)],
               [(2, 3), (4, 3), (1, 2), (7, 2), (3, 0), (6, 2), (3, 1), (1, 1)]]

wenz_hands_3 = [[(2, 2), (6, 3), (3, 3), (3, 1), (5, 1), (6, 1), (7, 1), (3, 2)],
               [(1, 0), (1, 2), (3, 0), (7, 3), (5, 0), (0, 1), (2, 0), (5, 2)],
               [(4, 1), (0, 2), (4, 2), (7, 2), (0, 0), (4, 3), (1, 3), (4, 0)],
               [(6, 0), (2, 1), (5, 3), (6, 2), (2, 3), (0, 3), (7, 0), (1, 1)]]

wenz_hands_4 = [[(3, 2), (7, 1), (6, 1), (1, 1), (2, 0), (7, 0), (3, 3), (6, 2)],
               [(4, 2), (4, 0), (3, 1), (7, 2), (5, 3), (1, 0), (2, 1), (0, 0)],
               [(6, 3), (5, 0), (0, 2), (6, 0), (7, 3), (5, 1), (1, 2), (0, 3)],
               [(0, 1), (4, 1), (5, 2), (2, 3), (2, 2), (4, 3), (1, 3), (3, 0)]]

wenz_hands_5 = [[(7, 1), (2, 2), (0, 0), (7, 0), (3, 0), (3, 3), (5, 3), (6, 0)],
               [(4, 0), (3, 1), (6, 2), (1, 3), (0, 3), (4, 3), (5, 0), (2, 1)],
               [(7, 3), (6, 1), (4, 2), (2, 3), (7, 2), (1, 1), (6, 3), (5, 2)],
               [(3, 2), (1, 2), (0, 2), (2, 0), (4, 1), (5, 1), (0, 1), (1, 0)]]
wenz_proposals = [(2, None), (0, None), (0, None), (0, None)]

list_player_hands_partner = [partner_hands_1, partner_hands_2, partner_hands_3, partner_hands_4, partner_hands_5,
                             partner_hands_6, partner_hands_7, partner_hands_8, partner_hands_9, partner_hands_10]
list_proposals_partner = [partner_proposals_1, partner_proposals_2, partner_proposals_3, partner_proposals_4,
                          partner_proposals_5, partner_proposals_6, partner_proposals_7, partner_proposals_8,
                          partner_proposals_9, partner_proposals_10]

list_player_hands_solo = [solo_hands_1, solo_hands_2, solo_hands_3, solo_hands_4, solo_hands_5]
list_proposals_solo = [solo_proposals_1, solo_proposals_2, solo_proposals_3, solo_proposals_4, solo_proposals_5]

list_player_hands_wenz = [wenz_hands_1, wenz_hands_2, wenz_hands_3, wenz_hands_4, wenz_hands_5]
list_proposals_wenz = [wenz_proposals for i in range(len(list_player_hands_wenz))]

list_player_hands = list_player_hands_partner + list_player_hands_wenz + list_player_hands_solo
list_proposals = list_proposals_partner + list_proposals_wenz + list_proposals_solo




sample_game_states_partner = []

for player_hands, mode_proposals in zip(list_player_hands_partner, list_proposals_partner):
    state = define_game_state(player_hands=player_hands, mode_proposals=mode_proposals, leading_player_index=0)
    sample_game_states_partner.append(state)

sample_game_states_wenz = []

for player_hands, mode_proposals in zip(list_player_hands_wenz, list_proposals_wenz):
    state = define_game_state(player_hands=player_hands, mode_proposals=mode_proposals, leading_player_index=0)
    sample_game_states_partner.append(state)

sample_game_states_solo = []

for player_hands, mode_proposals in zip(list_player_hands_solo, list_proposals_solo):
    state = define_game_state(player_hands=player_hands, mode_proposals=mode_proposals, leading_player_index=0)
    sample_game_states_partner.append(state)

sample_game_states = sample_game_states_partner + sample_game_states_wenz + sample_game_states_solo
