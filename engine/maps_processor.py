from engine.game_objects import Player

from dataclasses import dataclass


@dataclass
class SinglePlayerMap:
    # Must be positive
    game_field_size_x: int
    game_field_size_y: int

    player: Player


class RawMapsContainer:  # pragma: no cover
    @staticmethod
    def get_map_1() -> SinglePlayerMap:
        """Player only at (10, 10) position"""
        return SinglePlayerMap(700, 700, Player(10, 10))
