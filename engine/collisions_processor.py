from typing import List, Optional, TypeVar, Union
from enum import Enum
from dataclasses import dataclass
from itertools import chain as itertools_chain

from maps.maps_processor import GameMap
from engine.game_objects import (
    MovableObject,
    GameObject,
    Vector2D,
    PaintingConst,
    Player,
    ImmovableObject,
    AbstractBuff)
from engine import ApplicationException


class CollisionsProcessor:
    _game_map: GameMap

    # Result list of collisions in current iteration
    _result_collisions: List['Collision']

    GameObject = TypeVar('GameObject', covariant=True)

    def __init__(self, input_map: GameMap):
        self._game_map = input_map

    def get_collisions(
            self,
            moving_object: MovableObject,
            moving_vector: Vector2D) -> List['Collision']:
        """Main collisions acquiring method

        If there is no collisions then empty list is returned
        """
        self._result_collisions = []

        # Optimization: 'Middle' phase where every two objects' circles
        #  collision is checked. Every game object have its circle that
        #  contains this object. It is needed to compare square of sum of
        #  two radiuses and sum of squares of vector between centers of two
        #  circles. (Not root in second case for more performance)

        # 'Narrow' phase with detailed check
        if isinstance(moving_object, Player):
            self._check_player_collisions(
                moving_object,
                moving_vector,
                # Just all non-interface objects in case of no 'middle' phase
                list(itertools_chain(
                    self._game_map.movable_objects,
                    self._game_map.immovable_objects)))

        else:
            raise CollisionsProcessorException(
                'While processing [get_collisions] method, '
                'got [moving_object] with unknown type: '
                + moving_object.__class__.__name__)

        return self._result_collisions

    def _check_player_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            potentially_collided_objects:
            List[Union[MovableObject, ImmovableObject]]):
        self._check_player_with_borders_collisions(
            player, moving_vector)

        for game_object in potentially_collided_objects:
            if game_object is player:
                continue

            elif isinstance(game_object, AbstractBuff):
                self._check_player_with_buff_collisions(
                    player, moving_vector, game_object)

            # elif isinstance(game_object, BasicPlatform):
            #     self._check_player_with_basic_platform_collisions(
            #         player, moving_vector, game_object)

            else:
                raise CollisionsProcessorException(
                    "While processing [_check_player_collisions] method, "
                    "got [some_object] with unknown type: "
                    + game_object.__class__.__name__)

    def _check_player_with_borders_collisions(
            self,
            player: Player,
            moving_vector: Vector2D):
        # Horizontal
        if (player.location.x + PaintingConst.PLAYER_SIDE_LENGTH
                + moving_vector.x > self._game_map.game_field_size.x):
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_RIGHT, None))

        elif player.location.x + moving_vector.x < 0:
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_LEFT, None))

        # Vertical
        if (player.location.y + PaintingConst.PLAYER_SIDE_LENGTH
                + moving_vector.y > self._game_map.game_field_size.y):
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_GROUND, None))

        elif player.location.y + moving_vector.y < 0:
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_TOP, None))

    def _check_player_with_buff_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            buff: AbstractBuff):
        player_new_left_border: float = player.location.x + moving_vector.x
        player_new_right_border: float = (
            player.location.x
            + PaintingConst.PLAYER_SIDE_LENGTH
            + moving_vector.x)
        player_new_top_border: float = player.location.y + moving_vector.y
        player_new_bottom_border: float = (
            player.location.y
            + PaintingConst.PLAYER_SIDE_LENGTH
            + moving_vector.y)

        if (player_new_right_border >= buff.location.x
                and player_new_left_border
                <= buff.location.x + PaintingConst.BUFF_SIDE_LENGTH
                and player_new_bottom_border >= buff.location.y
                and player_new_top_border
                <= buff.location.y + PaintingConst.BUFF_SIDE_LENGTH
                and not buff.buff_is_charging):
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BUFF, buff))

    # TODO: Implement [_check_player_with_basic_platform_collisions]
    # def _check_player_with_basic_platform_collisions(
    #         self,
    #         player: Player,
    #         moving_vector: Vector2D,
    #         basic_platform: BasicPlatform):
    #     if (player.location.y + PaintingConst.PLAYER_SIDE_LENGTH
    #             < basic_platform.location.y
    #             <= player.location.y + PaintingConst.PLAYER_SIDE_LENGTH
    #             + moving_vector.y
    #             and player.location.x + PaintingConst.PLAYER_SIDE_LENGTH
    #             >= basic_platform.location.x
    #             and player.location.x
    #             <= basic_platform.location.x + basic_platform.get_width()):
    #         self._result_collisions.append(
    #             Collision(player, GameEvent.PLAYER_GROUND, basic_platform))


@dataclass
class Collision:
    moving_object: MovableObject
    game_event: 'GameEvent'

    # May be 'None'. For example, if game object is out of game field's borders
    collided_object: Optional[GameObject]


class GameEvent(Enum):
    """Enumerates all collision events that can occur
    """
    PLAYER_BORDERS_RIGHT = object()
    PLAYER_BORDERS_LEFT = object()
    PLAYER_BORDERS_TOP = object()

    # Player/borders_bottom OR Player/BasicPlatform
    PLAYER_GROUND = object()

    PLAYER_BUFF = object()


class CollisionsProcessorException(ApplicationException):
    pass
