from dataclasses import dataclass, field as dataclass_field
from typing import List, Optional


@dataclass
class GameObject:
    # Left top pixel location
    location: 'Vector2D'
    should_be_despawned: bool = dataclass_field(default=False)


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


class BasicPlatform(ImmovableObject):
    """Rectangle on which Player can walk"""
    # Width > 0 => size to the right from location, height > 0 => to the
    # bottom. If negative then to opposite directions
    #
    # Width and height may be negative ONLY in process of creating specific
    # basic platform inside map editor when left mouse button is held down.
    # Note that if basic platform have negative width/height then collisions
    # with player WON'T BE PROCESSED CORRECTLY
    #
    # Improvement: Constant width/height when basic platform is fully created.
    #  Add field 'size_is_changing' + property check for that field for map
    #  editor's size changing?
    #  OR
    #  Create new basic platform every time when size is changing in process
    #  of mouse motion?
    width: int
    height: int

    def __init__(self, in_width: int, in_height: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = in_width
        self.height = in_height


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


class ProjectileObject(MovableObject):
    _moving_vector: 'Vector2D'
    # Improvement: fired_player: Player

    def __init__(self, in_moving_vector: 'Vector2D', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._moving_vector = Vector2D(in_moving_vector.x, in_moving_vector.y)

    @property
    def moving_vector(self) -> 'Vector2D':
        return self._moving_vector


@dataclass
class HandgunProjectile(ProjectileObject):
    """Handgun projectile

    Small sized circle that just flies forward with average speed
    """


@dataclass
class MachineGunProjectile(ProjectileObject):
    """Machine gun projectile

    Average sized circle that flies forward with high speed with a chance of
    firing projectile with some angle from actual cursor direction
    """
    # Angle can scatter in this abs radius from zero
    ANGLE_SCATTER_RADIUS: int = 10


# Improvement: [InterfaceObject] class
# class InterfaceObject(GameObject):
#     """Abstraction for exact rendering order
#
#     Rendering order:
#     1. Interface objects
#     2. Immovable objects
#     3. Movable objects
#     """
#     pass


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

    # Buff is a square
    BUFF_SIDE_LENGTH: int = 25

    # Handgun projectile is a circle
    HANDGUN_PROJECTILE_DIAMETER: int = 7

    # Machine gun projectile is a circle
    MACHINE_GUN_PROJECTILE_DIAMETER: int = 12
