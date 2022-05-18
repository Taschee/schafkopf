import pygame

from schafkopf.game_modes import NO_GAME
from schafkopf.pygame_gui.BiddingOption import get_bidding_option_as_text
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame
from schafkopf.pygame_gui.colors import WHITE, BLACK


class ResultWidget(pygame.Surface):
    def __init__(self, schafkopf_game: SchafkopfGame, width: int, height: int):
        super().__init__((width, height))
        self.set_alpha(180)
        self.fill(WHITE)
        heading = self.get_heading_text(schafkopf_game)
        self.blit(heading, (self.get_width() // 2 - heading.get_width() // 2, 10))

    def get_heading_text(self, schafkopf_game: SchafkopfGame):
        results = schafkopf_game.get_results()
        if results.game_mode[0] == NO_GAME:
            text = "Niemand wollte spielen"
        else:
            if results.declaring_player in results.winners:
                text = f'{get_bidding_option_as_text(schafkopf_game.game_state["game_mode"])} gewonnen!'
            else:
                text = f'{get_bidding_option_as_text(schafkopf_game.game_state["game_mode"])} verloren!'
        font = pygame.font.Font(None, int(self.get_height() * 10 // 100))
        return font.render(text, True, BLACK)
