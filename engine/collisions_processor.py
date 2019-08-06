from maps.maps_processor import GameMap
from engine.game_objects import GameObject, Vector2D

from typing import Dict, Callable, List
from enum import Enum


class GameEvent(Enum):
    """Enumerates all events that can occur in process of game object moving

    OK is the only event that can be caused by any game object moving. Every other
    game event strictly refers to only one game object that caused this event"""
    OK = object()

    # TODO: Teleport Player close to game borders. Not just leave Player still
    PLAYER_IS_OUT_HORIZONTALLY = object()
    PLAYER_IS_OUT_VERTICALLY = object()
    PLAYER_IS_OUT_DIAGONALLY = object()


class CollisionsProcessor:
    """Class realize collision model in the game"""

    def __init__(self, input_map: GameMap):
        self._game_map = input_map

    class Collision:
        moving_object: GameObject
        game_event: GameEvent
        # May be None. For example, if game object is out of game field's borders
        collided_object: GameObject

    _game_map: GameMap
    _get_collision_switch: Dict[
        str,
        Callable[[GameObject, Vector2D], List[Collision]]] = {

    }

    def get_collision(self, moving_object: GameObject, moving_vector: Vector2D)\
            -> List[Collision]:
        """Main collision acquiring method"""
        pass
