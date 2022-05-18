import pygame

from schafkopf.game_modes import NO_GAME
from schafkopf.pygame_gui.BiddingOption import get_bidding_option_as_text
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame, GameResult
from schafkopf.pygame_gui.colors import WHITE, BLACK


class ResultWidget(pygame.Surface):
    def __init__(self, schafkopf_game: SchafkopfGame, width: int, height: int):
        super().__init__((width, height))
        self.set_alpha(180)
        self.fill(WHITE)
        results = schafkopf_game.get_results()
        self._add_heading(results)
        self._add_payouts(results)

    def _add_heading(self, results):
        heading = self._get_heading_text(results)
        self.blit(heading, self._get_heading_position(heading.get_width()))

    def _get_heading_position(self, heading_width):
        return self.get_width() // 2 - heading_width // 2, 10

    def _get_heading_text(self, results: GameResult):
        if results.game_mode[0] == NO_GAME:
            text = "Niemand wollte spielen"
        else:
            if results.declaring_player in results.winners:
                text = f'{get_bidding_option_as_text(results.game_mode)} gewonnen!'
            else:
                text = f'{get_bidding_option_as_text(results.game_mode)} verloren!'
        font = pygame.font.Font(None, self._get_heading_height())
        return font.render(text, True, BLACK)

    def _get_heading_height(self):
        return int(self.get_height() * 15 // 100)

    def _get_payout_height(self):
        return int(self.get_height() * 10 // 100)

    def _add_payouts(self, results):
        payout_height = self._get_payout_height()
        positions = self._get_payout_positions(payout_height)
        font = pygame.font.Font(None, self._get_payout_height())
        for i, payout in enumerate(results.payouts):
            payout_widget = font.render(str(payout), True, BLACK)
            self.blit(payout_widget, positions[i])


    def _get_payout_positions(self, payout_height):
        offset = 100
        payout_width = 50
        width, height = self.get_size()
        heading_height = self._get_heading_height()
        return [
            (width // 2 - payout_width // 2, height - payout_height - offset),
            (offset, (height + heading_height - payout_height) // 2),
            (width // 2 - payout_width // 2, heading_height + offset),
            (width - payout_width - offset, (height + heading_height - payout_height) // 2)
        ]
