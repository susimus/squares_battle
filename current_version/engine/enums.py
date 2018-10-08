from enum import Enum


class GameObjectType(Enum):
    '''Class contains game object types'''
    Field = 0
    Player = 1


class MoveDirection(Enum):
    '''CLass contains available move directions'''
    Right = 0
    Down = 1
    Left = 2
    Up = 3
