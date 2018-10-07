#  pragma: no cover
from enum import Enum


class GameObjectType(Enum):
    Field = 0
    Player = 1


class MoveDirection(Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3