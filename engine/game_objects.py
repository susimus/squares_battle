from dataclasses import dataclass, field as dataclass_field
from typing import List, Optional


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
    _recharge_time: int = dataclass_field(default=200)

    _is_charging: bool = dataclass_field(default=False)
    _charge_time_start: int = dataclass_field(default=0)
    _player_captor: Optional['Player'] = dataclass_field(default=None)

    def capture_this_buff(
            self,
            charge_time_start: int,
            player_captor: 'Player'):
        self._is_charging = True
        self._charge_time_start = charge_time_start
        self._player_captor = player_captor

        self._player_captor.current_buffs.append(self)

    def check_buff_expiration(self, current_time: int):
        if (self._is_charging
                and current_time - self._charge_time_start
                >= self._recharge_time):
            self._player_captor.current_buffs.remove(self)

            self._is_charging = False

    def is_charging(self):
        return self._is_charging


class SpeedUpBuff(AbstractBuff):
    """Increase move speed of Player"""
    pass


class JumpHeightUpBuff(AbstractBuff):
    pass


@dataclass
class BasicPlatform(ImmovableObject):
    """Rectangle on which Player can walk"""
    _width: int
    _height: int

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height


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

    # Buffs are squares
    BUFF_SIDE_LENGTH: int = 25
