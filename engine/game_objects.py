from dataclasses import dataclass, field as dataclass_field
from typing import List


@dataclass
class GameObject:
    # Left top pixel position
    location: 'Vector2D'


class ImmovableObject(GameObject):
    """Abstraction for exact rendering order

    Rendering order:
    1. Interface objects
    2. Immovable objects
    3. Movable objects
    """
    pass


@dataclass
class AbstractBuff(ImmovableObject):
    # Time in game loop iterations
    _recharge_time: int = dataclass_field(default=100)

    buff_is_charging: bool = dataclass_field(default=False)
    charge_time_passed: int = dataclass_field(default=0)

    def get_recharge_time(self):
        return self._recharge_time


class SpeedUpBuff(AbstractBuff):
    """Increase move speed of Player"""
    pass


class JumpHeightUpBuff(AbstractBuff):
    pass

# TODO: Implement [BasicPlatform]
# @dataclass
# class BasicPlatform(ImmovableObject):
#     """Rectangle on which Player can walk"""
#     _width: int
#     _height: int
#
#     def get_width(self) -> int:
#         return self._width
#
#     def get_height(self) -> int:
#         return self._height


class MovableObject(GameObject):
    """Abstraction for exact rendering order

    Rendering order:
    1. Interface objects
    2. Immovable objects
    3. Movable objects
    """
    pass


@dataclass
class Player(MovableObject):
    current_buffs: List[AbstractBuff] = dataclass_field(default_factory=list)


# TODO: Implement [BasicProjectile]
@dataclass
class BasicProjectile(MovableObject):
    """Small projectile-sphere that just flies forward with average speed"""
    fired_player: Player


# TODO: Implement [InterfaceObject]
class InterfaceObject(GameObject):
    """Abstraction for exact rendering order

    Rendering order:
    1. Interface objects
    2. Immovable objects
    3. Movable objects
    """
    pass


@dataclass
class Vector2D:
    """Vector of two coordinates: X, Y

    All positions or position modifiers in game should be vectors of two
    coordinates
    """
    x: float
    y: float

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)


class PaintingConst:
    # Player is a square
    PLAYER_SIDE_LENGTH: int = 45

    # Optimization: Exact length
    # Buffs are squares
    BUFF_SIDE_LENGTH: int = 20
