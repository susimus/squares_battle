from dataclasses import dataclass


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


@dataclass
class GameObject:
    # Left top pixel position
    current_position: Vector2D


class ImmovableObject(GameObject):
    """Abstraction for exact rendering order

    Rendering order:
    1. Interface objects
    2. Immovable objects
    3. Movable objects
    """
    pass


# TODO: Implement [BasicPlatform]
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
    pass


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


class PaintingConst:
    # Player is a square
    PLAYER_SIDE_LENGTH = 45
