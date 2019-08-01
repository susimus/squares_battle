from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameObject:
    """Main "game object" abstraction"""
    # Left top painted pixel position
    # Optimize: Really left top? Check tkinter painting
    current_position_x: int
    current_position_y: int


@dataclass
class MovableObject(GameObject):
    """All objects that can be moved. For example: Player, BasicProjectile"""
    def modify_location(self, modifier: Tuple[int, int]) -> None:
        self.current_position_x += modifier[0]
        self.current_position_y += modifier[1]


@dataclass
class Player(MovableObject):
    """Player abstraction"""
    pass


@dataclass
class BasicProjectile(MovableObject):  # TODO
    """Small projectile-sphere that just flies forward with average speed"""
    fired_by_player: bool
