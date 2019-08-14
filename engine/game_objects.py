from dataclasses import dataclass


@dataclass
class Vector2D:
    """Vector of two coordinates: X, Y

    All positions or position modifiers in game should be vectors of two coordinates
    """
    x: float = 0
    y: float = 0

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)


@dataclass
class GameObject:
    """Main "game object" abstraction"""
    # Left top pixel position
    current_position: Vector2D = Vector2D()


@dataclass
class BasicProjectile(GameObject):  # TODO
    """Small projectile-sphere that just flies forward with average speed"""
    # If '0' then projectile fired by mob
    # If '1' or higher then fired by Player. Number specifies Player instance
    fired_by_player: int = 1


# TODO: class Platform(GameObject)
#  Should be painted only in gui method 'init'


# TODO: class InterfaceObject(GameObject)


@dataclass
class MortalObject(GameObject):
    """Objects that can be destroyed during gameplay"""
    current_position: Vector2D = Vector2D()


@dataclass
class Player(MortalObject):
    """Player abstraction"""
    current_position: Vector2D = Vector2D()


class PaintingConst:
    # Player is a square
    PLAYER_SIDE_LENGTH = 45
