from dataclasses import dataclass


@dataclass
class Vector2D:
    """Vector of two coordinates: X, Y

    All positions or position modifiers in game should be vectors of two
    coordinates
    """
    x: float = 0
    y: float = 0

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)


@dataclass
class GameObject:
    # Left top pixel position
    current_position: Vector2D


# TODO: Implement [BasicProjectile]
@dataclass
class BasicProjectile(GameObject):
    """Small projectile-sphere that just flies forward with average speed"""
    # Always fired by some Player. Number specifies Player instance
    fired_by_player: int


# TODO: Implement [BasicPlatform]
class BasicPlatform(GameObject):
    """Rectangle on which Player can walk"""
    _width: int
    _height: int

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height


# TODO: Implement [InterfaceObject]
class InterfaceObject(GameObject):
    pass


@dataclass
class Player(GameObject):
    pass


class PaintingConst:
    # Player is a square
    PLAYER_SIDE_LENGTH = 45
