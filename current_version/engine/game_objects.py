from enum import Enum
from dataclasses import dataclass


@dataclass
class GameObject:
    """Data class that realizes main "game object" abstraction"""
    movable: bool


@dataclass
class GameField(GameObject):
    """Data class that realizes game field abstraction"""
    size: tuple


@dataclass
class Player(GameObject):
    """Data class that realizes player abstraction"""
    current_position: tuple  # Left top pixel position. Player is a square


class MoveDirection(Enum):
    """CLass contains available move directions"""
    Right = 0
    Down = 1
    Left = 2
    Up = 3
