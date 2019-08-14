from typing import Dict, Callable, List, TypeVar, Optional
from enum import Enum

from maps.maps_processor import GameMap
from engine.game_objects import *


class GameEvent(Enum):
    """Enumerates all events that can occur in process of game object moving"""
    PLAYER_IS_OUT_RIGHT = object()
    PLAYER_IS_OUT_LEFT = object()
    PLAYER_IS_OUT_TOP = object()
    PLAYER_IS_OUT_BOTTOM = object()


@dataclass
class Collision:
    """Collision abstraction for CollisionsProcessor"""
    moving_object: GameObject
    game_event: GameEvent

    # May be 'None'. For example, if game object is out of game field's borders
    collided_object: Optional[GameObject]


class CollisionsProcessor:
    """Realises collision model in the game"""

    def __init__(self, input_map: GameMap):
        self._game_map = input_map

        # Add narrow check functions into switch here
        self._narrow_check_switch = {
            "Player": self._check_player_collisions
        }

    _game_map: GameMap

    GameObject = TypeVar('GameObject', covariant=True)
    NarrowPhaseFunc = Callable[
        [GameObject,  # Moving object
         Vector2D,  # Moving vector
         List[GameObject]  # Possibly collided objects
         ],
        List[Collision]]
    _narrow_check_switch: Dict[str, NarrowPhaseFunc]

    def get_collisions(
            self,
            moving_object: GameObject,
            moving_vector: Vector2D) -> List[Collision]:
        """Main collisions acquiring method

        If there is no collisions then empty list is returned"""

        # TODO: 'Middle' phase where every two objects' circles collision is
        #  checked. Every game object have its circle that contains this
        #  object. It is needed to compare square of sum of two radiuses and
        #  sum of squares of vector between centers of two circles. (Not root
        #  in second case for more performance)

        # 'Narrow' phase with detailed check
        narrow_phase_func = self._narrow_check_switch.get(
            moving_object.__class__.__name__, None)
        if narrow_phase_func is None:
            raise ValueError(
                'Got unknown class of [moving_object]: '
                + moving_object.__class__.__name__)

        return narrow_phase_func(moving_object, moving_vector, [])

    def _check_player_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            possibly_collided_objects: List[GameObject]) -> List[Collision]:
        """All Player collisions checks are here"""
        result_collisions: List[Collision] = []

        # Game borders collisions check
        if (player.current_position.x + PaintingConst.PLAYER_SIDE_LENGTH
                + moving_vector.x > self._game_map.game_field_size.x):
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_RIGHT, None))
        elif player.current_position.x + moving_vector.x < 0:
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_LEFT, None))
        if (player.current_position.y + PaintingConst.PLAYER_SIDE_LENGTH
                + moving_vector.y > self._game_map.game_field_size.y):
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_BOTTOM, None))
        elif player.current_position.y + moving_vector.y < 0:
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_TOP, None))

        # TODO: Other collisions check

        return result_collisions
