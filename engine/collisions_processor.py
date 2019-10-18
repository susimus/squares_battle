from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

from maps.maps_processor import GameMap
from engine.game_objects import (
    MovableObject, GameObject, Vector2D, PaintingConst, Player)
from engine import ApplicationException


class CollisionsProcessor:
    _game_map: GameMap

    def __init__(self, input_map: GameMap):
        self._game_map = input_map

    def get_collisions(
            self,
            moving_object: GameObject,
            moving_vector: Vector2D) -> List['Collision']:
        """Main collisions acquiring method

        If there is no collisions then empty list is returned
        """
        # Optimization: 'Middle' phase where every two objects' circles
        #  collision is checked. Every game object have its circle that
        #  contains this object. It is needed to compare square of sum of
        #  two radiuses and sum of squares of vector between centers of two
        #  circles. (Not root in second case for more performance)

        # 'Narrow' phase with detailed check

        result_collisions: List[Collision]

        if isinstance(moving_object, Player):
            result_collisions = self._check_player_collisions(
                moving_object, moving_vector)
        else:
            raise CollisionsProcessorException(
                'While processing [get_collisions] method, '
                'got [moving_object] with unknown type: '
                + moving_object.__class__.__name__)

        return result_collisions

    def _check_player_collisions(
            self,
            player: Player,
            moving_vector: Vector2D) -> List['Collision']:
        result_collisions: List[Collision] = []

        self._check_player_with_borders_collisions(
            player, moving_vector, result_collisions)

        # TODO: Other collisions check

        return result_collisions

    def _check_player_with_borders_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            result_collisions: List['Collision']):
        # Horizontal
        if (player.current_position.x + PaintingConst.PLAYER_SIDE_LENGTH
                + moving_vector.x > self._game_map.game_field_size.x):
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_RIGHT, None))

        elif player.current_position.x + moving_vector.x < 0:
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_LEFT, None))

        # Vertical
        if (player.current_position.y + PaintingConst.PLAYER_SIDE_LENGTH
                + moving_vector.y > self._game_map.game_field_size.y):
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_BOTTOM, None))

        elif player.current_position.y + moving_vector.y < 0:
            result_collisions.append(
                Collision(player, GameEvent.PLAYER_IS_OUT_TOP, None))


@dataclass
class Collision:
    moving_object: MovableObject
    game_event: 'GameEvent'

    # May be 'None'. For example, if game object is out of game field's borders
    collided_object: Optional[GameObject]


class GameEvent(Enum):
    """Enumerates all events that can occur in process of game object moving"""
    PLAYER_IS_OUT_RIGHT = object()
    PLAYER_IS_OUT_LEFT = object()
    PLAYER_IS_OUT_TOP = object()
    PLAYER_IS_OUT_BOTTOM = object()


class CollisionsProcessorException(ApplicationException):
    pass
