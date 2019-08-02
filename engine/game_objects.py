from engine.engine import Vector2D

from dataclasses import dataclass


@dataclass
class GameObject:
    """Main "game object" abstraction"""
    # Left top painted pixel position
    # Optimize: Really left top? Check tkinter painting
    current_position: Vector2D


@dataclass
class Player:
    """Player abstraction"""
    pass


@dataclass
class BasicProjectile:  # TODO
    """Small projectile-sphere that just flies forward with average speed"""
    fired_by_player: bool
