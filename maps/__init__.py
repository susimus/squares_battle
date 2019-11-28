from copy import deepcopy
from typing import Tuple

from engine.game_objects import *
from engine import ApplicationException


DEFAULT_RESOLUTION: Tuple[int, int] = (1000, 700)


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

    # Improvement: interface_objects: List[InterfaceObject]
    immovable_objects: List[ImmovableObject]
    movable_objects: List[MovableObject]

    def __init__(
            self,
            input_game_field_size: Vector2D,
            input_immovable_objects: List[ImmovableObject],
            input_movable_objects: List[MovableObject]):
        if input_game_field_size.x < 0 or input_game_field_size.y < 0:
            raise ApplicationException(
                'Got negative game field size in process of game map init: '
                + str(input_game_field_size))

        self.game_field_size = deepcopy(input_game_field_size)
        self.immovable_objects = deepcopy(input_immovable_objects)
        self.movable_objects = deepcopy(input_movable_objects)

    def remove_all_game_objects(self):
        self.immovable_objects = []
        self.movable_objects = []

    def set(self, input_game_map: 'GameMap'):
        self.movable_objects = input_game_map.movable_objects
        self.immovable_objects = input_game_map.immovable_objects


class RawMapsContainer:
    """Contains maps initializations via code"""
    @staticmethod
    def get_map_1() -> GameMap:
        """One player only"""
        return GameMap(
            Vector2D(*DEFAULT_RESOLUTION),
            [],
            [Player(Vector2D(10, 10))])

    @staticmethod
    def get_map_2() -> GameMap:
        """Player with three platforms"""
        return GameMap(
            Vector2D(*DEFAULT_RESOLUTION),
            [BasicPlatform(200, 30, Vector2D(400, 600)),  # Center
             BasicPlatform(20, 100, Vector2D(0, 600)),  # Left
             BasicPlatform(20, 100, Vector2D(980, 600))],  # Right
            [Player(Vector2D(101, 101))])

    @staticmethod
    def get_map_3() -> GameMap:
        """Player with two buffs"""
        return GameMap(
            Vector2D(*DEFAULT_RESOLUTION),
            [SpeedUpBuff(Vector2D(500, 550)),
             JumpHeightUpBuff(Vector2D(800, 550))],
            [Player(Vector2D(0, 0))])

    @staticmethod
    def get_map_4() -> GameMap:
        """Player with handgun and machine gun projectiles"""
        return GameMap(
            Vector2D(*DEFAULT_RESOLUTION),
            [],
            [Player(Vector2D(0, 0)),
             HandgunProjectile(Vector2D(0, 0), Vector2D(10, 10)),
             MachineGunProjectile(Vector2D(0, 0), Vector2D(100, 10))])
