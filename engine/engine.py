from maps.maps_processor import GameMap
from gui.gui import GameGUI, EventListener

from time import (
    time as current_time_in_seconds,
    sleep as time_sleep)
from threading import Thread
from typing import Set


class GameEngine(EventListener):
    """All game logic processes here"""

    def __init__(self, input_game_map: GameMap):
        self._game_map = input_game_map
        self._map_updater = self.MapUpdater(input_game_map)

#
# Event listener methods
#

    # All key codes of keys that are currently pressed. Without lock because modifying
    # appears only in 'event listener' methods
    _keysPressed: Set[int] = {}

    def key_released(self, key_code: int):
        self._keysPressed.remove(key_code)

    def key_pressed(self, key_code: int):
        self._keysPressed.add(key_code)

    _game_closed: bool = False

    def window_closed(self):
        pass

#
# Main game loop section
#

    class MapUpdater:
        """All map state updating logic is here"""
        _game_map: GameMap

        def __init__(self, input_map: GameMap):
            self._game_map = input_map

        def update_map(self):
            """Main method that should be invoked from game loop"""
            # TODO
            pass

    _gui: GameGUI = GameGUI()
    _game_loop_iterations_count: int = 0
    _game_map: GameMap
    _map_updater: MapUpdater

    def start_game(self):
        """Initialize game loop"""
        self._gui.init(self._game_map, self)

        Thread(target=self._game_loop).start()
        # Right here several renderings might be lost. Not so critical for debugging
        self._gui.run_gui_loop()

    @staticmethod
    def _time_alignment():
        """Time alignment for CPU power saving

        Игра работает в режиме 60 итераций игрового цикла (обновление И рендер уровня в
        одной итерации) в секунду.

        По сути, секунда разбита на 60 частей. Выравнивание происходит таким образом,
        что в начале каждой 1\60 части секунды должна начинаться КАЖДАЯ итерация
        игрового цикла. НЕТ гарантии, что при таком подходе не будет потеряна одна из
        1\60-ой частей секунды

        Таким образом, каждое обновление уровня происходит с рассчетом ТОЛЬКО на
        текущую 1/60 часть секунды. Это позволяет избавиться от дробных величин при
        модификации позиции движущихся объектов.
        """
        # All time below in milliseconds
        one_iteration_time: int = 1000 // 60
        millis_in_current_second: int = int(current_time_in_seconds() * 1000) % 1000
        time_sleep(
            (one_iteration_time - millis_in_current_second % one_iteration_time) / 1000)

    def _game_loop(self):
        """Game loop has 3 parts in order: update, render, time alignment"""
        while True:  # TODO: Change condition to 'game_is_not_closed'
            self._map_updater.update_map()
            # print(self._keysPressed)
            # Check here if game is not closed
            # self._gui.destroy()
            self._gui.render()

            self._time_alignment()

            self._game_loop_iterations_count += 1
