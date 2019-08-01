from engine.engine import GameVector

from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameObject:
    """Main "game object" abstraction"""
    current_position: GameVector  # Left top pixel position


@dataclass
class MovableObject(GameObject):
    """All objects that can be moved. For example: Player, BasicProjectile"""
    pass


@dataclass
class Player(MovableObject):
    """Data class that realizes player abstraction"""
    pass