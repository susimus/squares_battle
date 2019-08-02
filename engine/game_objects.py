from engine.engine import Vector2D

from dataclasses import dataclass


@dataclass
class GameObject:
    """Main "game object" abstraction"""
    # Left top painted pixel position
    # Optimize: Really left top? Check tkinter painting
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
