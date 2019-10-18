from typing import List
from copy import deepcopy

from engine.game_objects import (
    Player,
    Vector2D,
    BasicPlatform,
    ImmovableObject,
    MovableObject)
from engine import ApplicationException


class MapsProcessorException(ApplicationException):
    pass


class GameMap:
    """

    Rendering order:
    1. Interface objects
    2. Immovable objects
    3. Movable objects
    """
    # Size coordinates must be non-negative. Immutable when game field is
    # showing
    game_field_size: Vector2D

    # WouldBeBetter: Implement [interface_objects]
    immovable_objects: List[ImmovableObject]
    movable_objects: List[MovableObject]

    def __init__(
            self,
            input_game_field_size: Vector2D,
            input_immovable_objects: List[ImmovableObject],
            input_movable_objects: List[MovableObject]):
        if input_game_field_size.x < 0 or input_game_field_size.y < 0:
            raise MapsProcessorException(
                'Got negative game field size in process of game map init: '
                + str(input_game_field_size))

        self.game_field_size = deepcopy(input_game_field_size)
        self.immovable_objects = deepcopy(input_immovable_objects)
        self.movable_objects = deepcopy(input_movable_objects)


class RawMapsContainer:
    """Contains maps initializations via code"""
    @staticmethod
    def get_map_1() -> GameMap:
        return GameMap(
            Vector2D(1200, 700),
            [],
            [Player(Vector2D(10, 10))])

    # TODO: Implement [get_map2]
    @staticmethod
    def get_map2() -> GameMap:
        return GameMap(
            Vector2D(1200, 700),
            [BasicPlatform(Vector2D(0, 0), 100, 100)],
            [Player(Vector2D(101, 101))])
