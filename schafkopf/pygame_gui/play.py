from typing import List, Tuple

import pygame

from schafkopf.game_modes import NO_GAME
from schafkopf.pygame_gui.BiddingProposalWidget import BiddingProposalWidget
from schafkopf.pygame_gui.Button import Button
from schafkopf.pygame_gui.GameModeWidget import GameModeWidget
from schafkopf.pygame_gui.GameResult import GameResult
from schafkopf.pygame_gui.NextGameButton import NextGameButton
from schafkopf.pygame_gui.HiddenCardWidget import HiddenCardWidget
from schafkopf.pygame_gui.OpenCardWidget import OpenCardWidget
from schafkopf.pygame_gui.PlayerInfoWidget import PlayerInfoWidget
from schafkopf.pygame_gui.ResultsWidget import ResultsWidget
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame
from schafkopf.pygame_gui.Widget import Widget

pygame.init()
FONT = pygame.font.Font(None, 30)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1500, 1000))
screen_size = screen_width, screen_height = screen.get_size()
background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)

space_between = 15
card_size = card_width, card_height = HiddenCardWidget().rect.size

player_hand_position_top = screen_height * 95 / 100 - card_height
opposing_hand_position_top = screen_height * 5 / 100
neighboring_hand_edge_distance = screen_width * 5 / 100


def space_for_player_hand(num_cards):
    return num_cards * card_width + (num_cards - 1) * space_between


def player_hand_position_left(num_cards):
    return (screen_width - space_for_player_hand(num_cards)) / 2


def calculate_ith_card_position_player(i, player_hand):
    return (player_hand_position_left(len(player_hand)) + i * (card_width + space_between),
            player_hand_position_top)


def neighboring_hand_position_top(num_cards):
    return (screen_height - space_for_player_hand(num_cards)) / 2


def calculate_ith_card_position_first_opponent(num_cards, i):
    return (
        neighboring_hand_edge_distance,
        neighboring_hand_position_top(num_cards) + i * (card_width + space_between)
    )


def calculate_ith_card_position_second_opponent(num_cards, i):
    return (
        player_hand_position_left(num_cards) + i * (card_width + space_between),
        opposing_hand_position_top
    )


def calculate_ith_card_position_third_opponent(num_cards, i):
    return (
        screen_width - neighboring_hand_edge_distance - card_height,
        neighboring_hand_position_top(num_cards) + i * (card_width + space_between)
    )


bidding_option_position_left = int(screen_width * 40 / 100)
bidding_option_position_height = int(screen_height * 30 / 100)
font_size = screen_height // 25
bidding_option_space_between = font_size + 15

bidding_proposal_size = bidding_proposal_width, bidding_proposal_height = (screen_width // 10, screen_height // 20)

game_mode_position_human = (
    int(screen_width * 45 / 100),
    player_hand_position_top - space_between - bidding_proposal_height
)
game_mode_position_first_opp = (
    neighboring_hand_edge_distance + card_height + space_between,
    int(screen_height * 50 / 100)
)
game_mode_position_second_opp = (
    int(screen_width * 45 / 100),
    opposing_hand_position_top + space_between + card_height
)
game_mode_position_third_opp = (
    screen_width - neighboring_hand_edge_distance - card_height - bidding_proposal_width - space_between,
    int(screen_height * 50 / 100)
)
game_mode_positions = [
    game_mode_position_human, game_mode_position_first_opp, game_mode_position_second_opp, game_mode_position_third_opp
]

current_trick_human_pos = (
    screen_width // 2 - card_width // 2,
    screen_height // 2 + space_between
)
current_trick_first_opp_pos = (
    screen_width // 2 - 2 * card_width - space_between,
    screen_height // 2 - card_height // 2
)
current_trick_second_opp_pos = (
    screen_width // 2 - card_width // 2,
    screen_height // 2 - card_height - space_between
)
current_trick_third_opp_pos = (
    screen_width // 2 + card_width + space_between,
    screen_height // 2 - card_height // 2
)
current_trick_positions = [
    current_trick_human_pos, current_trick_first_opp_pos, current_trick_second_opp_pos, current_trick_third_opp_pos
]

player_info_size = player_info_width, player_info_height = (int(card_height * 1.5), card_height)
player_info_offset_horizontal = screen_width // 25
player_info_offset_vertical = screen_height // 25
player_info_human_position = (
    player_hand_position_left(8) + space_for_player_hand(8) + player_info_offset_horizontal,
    player_hand_position_top
)
player_info_first_opp_position = (
    neighboring_hand_edge_distance,
    neighboring_hand_position_top(8) + space_for_player_hand(8) + player_info_offset_vertical
)
player_info_second_opp_position = (
    player_hand_position_left(8) - player_info_width - player_info_offset_vertical,
    opposing_hand_position_top
)
player_info_third_opp_position = (
    screen_width - neighboring_hand_edge_distance - card_height,
    neighboring_hand_position_top(8) - player_info_height - player_info_offset_vertical
)
player_info_positions = [player_info_human_position, player_info_first_opp_position, player_info_second_opp_position,
                         player_info_third_opp_position]


class GameRunner:
    def __init__(self):
        self.leading_player_index = 0
        self.schafkopf_game = SchafkopfGame(leading_player_index=self.leading_player_index)
        self.total_scores = [0, 0, 0, 0]
        self.widgets = self.get_widgets()
        self.done = False

    def run(self):
        while not self.done:
            if self.human_player_needs_to_act():
                self.handle_events()
            else:
                pygame.time.wait(500)
                self.next_opponent_action()
            self.draw()
            clock.tick(30)

    def human_player_needs_to_act(self):
        return self.schafkopf_game.human_players_turn() or \
               self.schafkopf_game.finished() or \
               self.schafkopf_game.paused_on_last_trick

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
            if self.schafkopf_game.paused_on_last_trick and event.type == pygame.MOUSEBUTTONUP:
                self.schafkopf_game.unpause()
                self.update_widgets()
            buttons = [w for w in self.widgets if isinstance(w, Button)]
            for button in buttons:
                button.handle_event(event)

    def draw(self):
        screen.blit(background, (0, 0))
        for b in self.widgets:
            b.draw(screen)
        pygame.display.flip()

    def get_widgets(self) -> List[Widget]:
        return self.get_simple_widgets() + self.get_buttons()

    def update_widgets(self):
        self.widgets = self.get_widgets()

    def get_buttons(self) -> List[Button]:
        if self.schafkopf_game.finished():
            return [NextGameButton((0, 0), self.next_game)]
        else:
            buttons = self.get_player_card_widgets()
            if not self.schafkopf_game.bidding_is_finished():
                buttons += self.get_bid_option_widgets()
            return buttons

    def get_simple_widgets(self) -> List[Widget]:
        simple_widgets: List[Widget] = []
        simple_widgets += self.get_opponent_card_widgets()
        simple_widgets += self.get_player_info_widgets()
        if not self.schafkopf_game.bidding_is_finished():
            simple_widgets += self.get_bid_proposal_widgets()
        elif not self.schafkopf_game.finished():
            simple_widgets.append(self.get_game_mode_widget())
            simple_widgets += self.get_current_trick_widgets()
        else:
            simple_widgets.append(self.get_results_widget())
        return simple_widgets

    def get_player_card_widgets(self) -> List[Button]:
        if self.schafkopf_game.bidding_is_finished() and self.schafkopf_game.human_players_turn():
            return self.get_player_cards_on_players_turn()
        else:
            return self.get_player_cards_without_possible_actions()

    def get_player_cards_on_players_turn(self):
        player_hand = self.schafkopf_game.get_player_hand()
        possible_cards = self.schafkopf_game.possible_cards()
        player_cards: List[OpenCardWidget] = []
        for i, card_encoded in enumerate(player_hand):
            if card_encoded in possible_cards:
                player_cards.append(
                    OpenCardWidget(
                        topleft=calculate_ith_card_position_player(i, player_hand),
                        card_encoded=card_encoded,
                        hover_effect=True,
                        callback=self.next_player_card_callback(card_encoded)
                    )
                )
            else:
                player_cards.append(
                    OpenCardWidget(
                        topleft=calculate_ith_card_position_player(i, player_hand),
                        card_encoded=card_encoded,
                        hover_effect=False,
                    )
                )
        return player_cards

    def get_player_cards_without_possible_actions(self):
        player_hand = self.schafkopf_game.get_player_hand()
        return [
            OpenCardWidget(
                topleft=calculate_ith_card_position_player(i, player_hand),
                card_encoded=card_encoded,
                hover_effect=False,
            ) for i, card_encoded in enumerate(player_hand)
        ]

    def get_opponent_card_widgets(self) -> List[Widget]:
        first_opponent_hand, second_opponent_hand, third_opponent_hand = self.schafkopf_game.get_opponent_hands()
        first_opponent_cards = [
            HiddenCardWidget(
                rotate=True,
                topleft=calculate_ith_card_position_first_opponent(len(first_opponent_hand), i)
            ) for i, _ in enumerate(first_opponent_hand)
        ]
        second_opponent_cards = [
            HiddenCardWidget(
                rotate=False,
                topleft=calculate_ith_card_position_second_opponent(len(second_opponent_hand), i)
            ) for i, _ in enumerate(second_opponent_hand)
        ]
        third_opponent_cards = [
            HiddenCardWidget(
                rotate=True,
                topleft=calculate_ith_card_position_third_opponent(len(third_opponent_hand), i)
            ) for i, _ in enumerate(third_opponent_hand)
        ]
        return first_opponent_cards + second_opponent_cards + third_opponent_cards

    def get_current_trick_widgets(self) -> List[Widget]:
        current_trick_cards = self.schafkopf_game.get_current_trick()
        current_trick = []
        for i, card_encoded in enumerate(current_trick_cards):
            if card_encoded is not None:
                current_trick.append(
                    OpenCardWidget(
                        topleft=current_trick_positions[i],
                        card_encoded=card_encoded,
                        hover_effect=False,
                    )
                )
        return current_trick

    def get_bid_option_widgets(self) -> List[GameModeWidget]:
        if self.schafkopf_game.human_players_turn():
            possible_modes = self.schafkopf_game.possible_bids()
            return [
                GameModeWidget(
                    topleft=(bidding_option_position_left,
                             bidding_option_position_height + i * bidding_option_space_between),
                    bidding_option=option,
                    callback=self.make_proposal_callback(option),
                    font_size=font_size
                ) for i, option in enumerate(possible_modes)
            ]
        else:
            return []

    def get_results_widget(self) -> Widget:
        return ResultsWidget(
            topleft=(screen_width // 4, screen_height // 4),
            width=screen_width // 2,
            height=screen_height // 2,
            game_results=self.schafkopf_game.get_results()
        )

    def get_bid_proposal_widgets(self) -> List[Widget]:
        proposals = self.schafkopf_game.get_mode_proposals()
        return [BiddingProposalWidget(
            topleft=game_mode_positions[(self.leading_player_index + i) % 4],
            player_passes=proposal[0] == NO_GAME,
            width=bidding_proposal_width,
            height=bidding_proposal_height,
            font_size=font_size
        ) for i, proposal in enumerate(proposals)]

    def get_game_mode_widget(self) -> Widget:
        declaring_player = self.schafkopf_game.get_declaring_player()
        return GameModeWidget(
            topleft=game_mode_positions[declaring_player],
            bidding_option=self.schafkopf_game.get_game_mode(),
            clickable=False,
            font_size=font_size,
        )

    def get_player_info_widgets(self):
        return [
            PlayerInfoWidget(
                topleft=player_info_positions[i],
                player_index=i,
                score=self.total_scores[i],
                font_size=font_size,
                size=player_info_size
            ) for i in range(4)
        ]

    def next_player_card_callback(self, card_encoded: Tuple[int, int]):
        def callback():
            self.schafkopf_game.next_human_card(card_encoded)
            self.update_widgets()

        return callback

    def make_proposal_callback(self, mode_proposal: Tuple[int, int]):
        def callback():
            self.schafkopf_game.next_human_bid(mode_proposal)
            self.update_widgets()

        return callback

    def next_opponent_action(self):
        self.schafkopf_game.next_action()
        self.update_widgets()

    def next_game(self):
        self.update_total_scores(self.schafkopf_game.get_results())
        self.leading_player_index = (self.leading_player_index + 1) % 4
        self.schafkopf_game = SchafkopfGame(self.leading_player_index)
        self.update_widgets()

    def update_total_scores(self, game_results: GameResult):
        for i, payout in enumerate(game_results.payouts):
            self.total_scores[i] += payout


if __name__ == "__main__":
    GameRunner().run()
    pygame.quit()
