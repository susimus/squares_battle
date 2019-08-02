<<<<<<< HEAD
from engine.game_objects import Player, Vector2D
=======
from engine.game_objects import Player
from engine.engine import Vector2D
>>>>>>> 85f43be49d051b17e85ead7a9225a4c027d03420

from dataclasses import dataclass


@dataclass
<<<<<<< HEAD
class GameMap:
    # Coordinates must be positive. Immutable when game field is showing
    game_field_size: Vector2D

    # Single player for now
=======
class SinglePlayerMap:
    # Coordinates must be positive. Immutable when game field is showing
    game_field_size: Vector2D

>>>>>>> 85f43be49d051b17e85ead7a9225a4c027d03420
    player: Player
    # mobs: List[MortalObject]  # TODO


class RawMapsContainer:  # pragma: no cover
    @staticmethod
<<<<<<< HEAD
    def get_map_1() -> GameMap:
        """Player only at (10, 10) position of game field with size (1200, 700)"""
        return GameMap(Vector2D(1200, 700), Player(Vector2D(10, 10)))
=======
    def get_map_1() -> SinglePlayerMap:
        """Player only at (10, 10) position"""
        return SinglePlayerMap(Vector2D(700, 700), Player(Vector2D(10, 10)))
>>>>>>> 85f43be49d051b17e85ead7a9225a4c027d03420
