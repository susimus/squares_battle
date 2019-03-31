from enum import Enum


class GameObject:
    """Data class that realizes main "game object" abstraction"""
    def __init__(self,
                 object_type,
                 movable,
                 net_dimensions,
                 current_position,
                 cell_size):
        self.object_type = object_type
        self.movable = movable
        self.net_dimensions = net_dimensions
        self.current_position = current_position
        self.cell_size = cell_size


class GameObjectType(Enum):
    """Class contains game object types"""
    Field = 0
    Player = 1


class MoveDirection(Enum):
    """CLass contains available move directions"""
    Right = 0
    Down = 1
    Left = 2
    Up = 3
