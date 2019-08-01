from engine.game_objects import (
    GameObject,
    GameField,
    Player)


class RawMapsContainer:  # pragma: no cover
    """Data class that contains raw game maps"""
    @staticmethod
    def get_map_1():  # Just field 100x100 pixels and player at (0, 0)
        """Method gives raw map №1"""
        game_map = []

        game_map.append(
            GameField(True, (1, 2)))

        game_map += [GameObject(
            GameObjectType.Player,
            True,
            (1, 1),
            (0, 0),
            1)]

        return game_map
