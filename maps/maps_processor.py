from engine.game_objects import Player
from engine.engine import Vector2D

from dataclasses import dataclass


@dataclass
class GameMap:
    # Coordinates must be positive. Immutable when game field is showing
    game_field_size: Vector2D

    # Single player for now
    player: Player
    # mobs: List[MortalObject]  # TODO


class RawMapsContainer:  # pragma: no cover
    @staticmethod
    def get_map_1() -> GameMap:
        """Player only at (10, 10) position"""
        return GameMap(Vector2D(700, 700), Player(Vector2D(10, 10)))
