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
    current_position: Vector2D


# class Projectile(GameObject)


@dataclass
class BasicProjectile(GameObject):  # TODO
    """Small projectile-sphere that just flies forward with average speed"""
    fired_by_player: bool


# class Platform(GameObject) # Should be painted only in gui method 'init'


# class InterfaceObject(GameObject)


@dataclass
class MortalObject(GameObject):  # TODO
    """Objects that can be destroyed during gameplay"""
    pass


@dataclass
class Player(MortalObject):
    """Player abstraction"""
    pass


class PaintingConst:
    # Player is a square
    PLAYER_SIDE_LENGTH = 45
