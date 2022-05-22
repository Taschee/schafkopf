from dataclasses import dataclass
from typing import Tuple, List, Union


@dataclass
class GameResult:
    payouts: Tuple[int, int, int, int]
    winners: List[int]
    declaring_player: Union[int, None]
    game_mode: tuple[int, Union[int, None]]
    offensive_players: List[int]
    offensive_points: int = 0
