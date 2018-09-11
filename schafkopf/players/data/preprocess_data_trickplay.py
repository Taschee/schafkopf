import pickle
from schafkopf.game_modes import SOLO, WENZ, PARTNER_MODE
from schafkopf.suits import HEARTS, ACORNS
from schafkopf.players.data.data_processing import switch_suits_player_hands, switch_card_suit, \
    switch_suits_played_cards
from schafkopf.ranks import OBER, UNTER


infilename = 'train_data.p'
solo_filename = 'train_data_solo.p'
wenz_filename = 'train_data_wenz.p'
partner_filename = 'train_data_partner.p'


def create_data_trickplay(infilename):
    with open(infilename, 'rb') as infile:
        while True:
            try:
                data_dic = pickle.load(infile)
                preprocess_game(data_dic)
            except EOFError:
                break
        return


def preprocess_game(data_dic):
    game_mode = data_dic['game_mode']
    if game_mode[0] == SOLO:
        transformed_dic = transform_solo(data_dic)
        with open(solo_filename, 'ab') as outfile:
            pickle.dump(transformed_dic, outfile)
    elif game_mode[0] == WENZ:
        transformed_dic = transform_wenz(data_dic)
        with open(wenz_filename, 'ab') as outfile:
            pickle.dump(transformed_dic, outfile)
    elif game_mode[0] == PARTNER_MODE:
        transformed_dic = transform_partner(data_dic)
        with open(partner_filename, 'ab') as outfile:
            pickle.dump(transformed_dic, outfile)


def transform_solo(data_dic):
    declaring_player = data_dic['declaring_player']
    game_suit = data_dic['game_mode'][1]
    # switch suits to HEARTS if necessary
    if game_suit != HEARTS:
        played_cards = switch_suits_played_cards(data_dic['played_cards'], game_suit, HEARTS)
        player_hands = switch_suits_player_hands(data_dic['player_hands'], game_suit, HEARTS)
    else:
        played_cards = data_dic['played_cards']
        player_hands = data_dic['player_hands']
    # set offensive player as player 0, and all relative positions accordingly
    played_cards = [(card, (player - declaring_player) % 4) for card, player in played_cards]
    # change player hand cards accordingly

    player_hands = [player_hands[(index + declaring_player) % 4] for index in range(4)]
    transformed_dic = {'player_hands': player_hands, 'played_cards': played_cards}
    return transformed_dic


def transform_wenz(data_dic):
    played_cards = data_dic['played_cards']
    declaring_player = data_dic['declaring_player']
    # set offensive player as player 0, and all relative positions accordingly
    played_cards = [(card, (player - declaring_player) % 4) for card, player in played_cards]
    # change player hand cards accordingly
    player_hands = [data_dic['player_hands'][(index + declaring_player) % 4] for index in range(4)]
    transformed_dic = {'player_hands': player_hands, 'played_cards': played_cards}
    return transformed_dic


def transform_partner(data_dic):
    declaring_player = data_dic['declaring_player']
    game_suit = data_dic['game_mode'][1]
    # switch suits to ACORNS if necessary
    if game_suit != ACORNS:
        played_cards = switch_suits_played_cards(data_dic['played_cards'], game_suit, ACORNS)
        player_hands = switch_suits_player_hands(data_dic['player_hands'], game_suit, ACORNS)
    else:
        played_cards = data_dic['played_cards']
        player_hands = data_dic['player_hands']
    # set offensive player as player 0, and all relative positions accordingly
    played_cards = [(card, (player - declaring_player) % 4) for card, player in played_cards]
    # change player hand cards accordingly
    player_hands = [player_hands[(index + declaring_player) % 4] for index in range(4)]
    transformed_dic = {'player_hands': player_hands, 'played_cards': played_cards}
    return transformed_dic


def main():
    create_data_trickplay(infilename)


if __name__ == '__main__':
    main()
