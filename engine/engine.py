from maps.maps_processor import GameMap
from gui.gui import GameGUI, EventListener
from engine.game_objects import *
from engine.collisions_processor import CollisionsProcessor, Collision, GameEvent

from time import (
    time as current_time_in_seconds,
    sleep as time_sleep)
from threading import Thread
from typing import Set, Dict, List


class GameEngine(EventListener):
    """All game logic processes here"""

    def __init__(self, input_game_map: GameMap):
        self._game_map = input_game_map
        self._map_updater = self.MapUpdater(input_game_map, self._keys_pressed)

#
# Event listener methods
#

    # All key codes of keys that are currently pressed. Without lock because modifying
    # appears only in 'event listener' methods. In all other places this field is just
    # read
    _keys_pressed: Set[int] = set()

    def key_pressed(self, key_code: int):
        """GUI thread enters this method to add pressed key to 'keysPressed' set"""
        self._keys_pressed.add(key_code)

    def key_released(self, key_code: int):
        """GUI thread enters this method to subtract pressed key from 'keysPressed' set"""
        self._keys_pressed.discard(key_code)

#
# Main game loop section
#

    class MapUpdater:
        """All map state updating logic is here"""

        class GameObjectsSpawner:
            """Accumulates all game objects spawning"""
            _game_map: GameMap

            # TODO

        class StateUpdater:
            """Accumulates all game objects state updating"""
            _game_map: GameMap
            _keys_pressed: Set[int]

            _collisions_processor: CollisionsProcessor

            def __init__(self, input_map: GameMap, input_keys_pressed: Set[int]):
                self._game_map = input_map
                self._keys_pressed = input_keys_pressed
                self._collisions_processor = CollisionsProcessor(input_map)

            _GRAVITY_MODIFIER: Vector2D = Vector2D(0, 5)

            def update_player_state(self):
                player_move_vector: Vector2D = (
                        self._get_input_move_vector() + self._GRAVITY_MODIFIER)
                if player_move_vector.x != 0 or player_move_vector.y != 0:
                    player_collisions: List[Collision] = (
                        self._collisions_processor.get_collisions(
                            self._game_map.player, player_move_vector))
                    for collision in player_collisions:
                        if collision.game_event is GameEvent.PLAYER_IS_OUT_RIGHT:
                            player_move_vector.x = 0
                            self._game_map.player.current_position.x = (
                                self._game_map.game_field_size.x
                                # '+ 1' for closest to border drawing
                                - PaintingConst.PLAYER_SIDE_LENGTH + 1)

                        elif collision.game_event is GameEvent.PLAYER_IS_OUT_LEFT:
                            player_move_vector.x = 0
                            self._game_map.player.current_position.x = 0

                        elif collision.game_event is GameEvent.PLAYER_IS_OUT_DOWN:
                            player_move_vector.y = 0
                            self._game_map.player.current_position.y = (
                                    self._game_map.game_field_size.y
                                    # '+ 1' for closest to border drawing
                                    - PaintingConst.PLAYER_SIDE_LENGTH + 1)

                        elif collision.game_event is GameEvent.PLAYER_IS_OUT_UP:
                            player_move_vector.y = 0
                            self._game_map.player.current_position.y = 0

                        else:
                            raise ValueError(
                                "Got unknown [game_event]: "
                                + collision.game_event.name)

                    self._game_map.player.current_position += player_move_vector

            _PLAYER_MOVE_SPEED: int = 5
            KEY_CODE_A: int = 65
            KEY_CODE_D: int = 68

            def _get_input_move_vector(self) -> Vector2D:
                """Method gets player's move vector from keyboard input"""
                input_move_vector: Vector2D = Vector2D(0, 0)
                # Copy in case if '_keys_pressed' will be modified during check
                keys_pressed_copy: Set[int] = set(self._keys_pressed)

                if self.KEY_CODE_A in keys_pressed_copy:
                    input_move_vector.x += -self._PLAYER_MOVE_SPEED

                if self.KEY_CODE_D in keys_pressed_copy:
                    input_move_vector.x += self._PLAYER_MOVE_SPEED

                return input_move_vector

        _state_updater: StateUpdater
        # _game_objects_spawner: GameObjectsSpawner

        def __init__(self, input_map: GameMap, input_keys_pressed: Set[int]):
            self._state_updater = self.StateUpdater(input_map, input_keys_pressed)

        def update_map(self):
            """Main update method that should be invoked from game loop"""
            self._state_updater.update_player_state()

    _gui: GameGUI = GameGUI()
    _map_updater: MapUpdater
    _game_loop_iterations_count: int = 0

    # At the same time one instance of game map can be either in the process of rendering
    # OR updating because of instance modifications in game loop thread. Game map
    # cloning would solve this restriction but it would be expensive and, actually,
    # useless: if some renders or updates are lost OR require too much time then
    # gameplay would be ruined anyway
    _game_map: GameMap

    def start_game(self):
        """Initialize game loop"""
        self._gui.init(self._game_map, self)

        Thread(target=self._game_loop, daemon=True).start()
        # Right here several renderings CANNOT be lost
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
        # Game loop is daemon thread so it will proceed until gui thread is closed
        while True:
            self._map_updater.update_map()

            self._gui.render()

            self._time_alignment()

            self._game_loop_iterations_count += 1
