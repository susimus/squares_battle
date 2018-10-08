from engine.game_object import GameObject
from engine.enums import GameObjectType


class RawMapsContainer:  # pragma: no cover
    '''Data class that contains raw game maps'''
    @staticmethod
    def get_map_1():  # Just field 10x10 and player at (0, 0)
        '''Method gives raw map №1'''
        game_map = []

        game_map += [GameObject(
            GameObjectType.Field,
            False,
            (10, 10),
            (0, 0),
            1)]

        game_map += [GameObject(
            GameObjectType.Player,
            True,
            (1, 1),
            (0, 0),
            1)]

        return game_map
