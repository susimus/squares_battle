from maps.maps_processor import GameMap
from engine.gui import GameGUI, EventListener
from engine.game_objects import *
from engine.collisions_processor import CollisionsProcessor, Collision, GameEvent

from time import (
    time as current_time_in_seconds,
    sleep as time_sleep)
from threading import Thread
from typing import Set, List


class GameEngine(EventListener):
    """All game logic processes here"""

    def __init__(self, input_game_map: GameMap):
        self._game_map = input_game_map
        self._map_updater = self.MapUpdater(input_game_map, self._keys_pressed)

    # All key codes of keys that are currently pressed. Without lock because modifying
    # appears only in 'event listener' methods. In all other places this field is just
    # read
    _keys_pressed: Set[int] = set()

    def key_pressed(self, key_code: int):  # pragma: no cover
        """GUI thread enters this method to add pressed key to 'keysPressed' set"""
        self._keys_pressed.add(key_code)

    def key_released(self, key_code: int):  # pragma: no cover
        """GUI thread enters this method to subtract pressed key from 'keysPressed' set"""
        self._keys_pressed.discard(key_code)

    class MapUpdater:
        """All map state updating logic is here"""

        def __init__(self, input_map: GameMap, input_keys_pressed: Set[int]):
            self._state_updater = self.StateUpdater(input_map, input_keys_pressed)

        # TODO
        # class GameObjectsSpawner:
        #     """All game objects spawning is here"""
        #     _game_map: GameMap

        class StateUpdater:
            """All game objects state updating is here"""
            _game_map: GameMap
            _keys_pressed: Set[int]

            _collisions_processor: CollisionsProcessor

            def __init__(self, input_map: GameMap, input_keys_pressed: Set[int]):
                self._game_map = input_map
                self._keys_pressed = input_keys_pressed
                self._collisions_processor = CollisionsProcessor(input_map)

            _jump_is_available: bool = False

            # Optimize: Change vertical velocity to 0 when PLAYER_IS_OUT_BOTTOM is gotten
            def update_player_state(self):  # pragma: no cover
                # Copy in case if '_keys_pressed' will be modified during check
                keys_pressed_copy: Set[int] = set(self._keys_pressed)
                player_move_vector: Vector2D = Vector2D()

                player_move_vector.x += self._get_horizontal_velocity(keys_pressed_copy)
                player_move_vector.y += self._get_vertical_velocity(keys_pressed_copy)

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

                        elif collision.game_event is GameEvent.PLAYER_IS_OUT_BOTTOM:
                            player_move_vector.y = 0
                            self._game_map.player.current_position.y = (
                                self._game_map.game_field_size.y
                                # '+ 1' for closest to border drawing
                                - PaintingConst.PLAYER_SIDE_LENGTH + 1)

                            self._jump_is_available = True

                        elif collision.game_event is GameEvent.PLAYER_IS_OUT_TOP:
                            player_move_vector.y = 0
                            self._game_map.player.current_position.y = 0

                        else:
                            raise ValueError(
                                "Got unknown [game_event]: "
                                + collision.game_event.name)

                    self._game_map.player.current_position += player_move_vector

            _PLAYER_MOVE_SPEED: int = 6

            _KEY_CODE_A: int = 65
            _KEY_CODE_D: int = 68

            def _get_horizontal_velocity(self, keys_pressed: Set[int]) -> float:
                """Method gets player's current horizontal velocity"""
                input_move_vector: Vector2D = Vector2D()

                if self._KEY_CODE_A in keys_pressed:
                    input_move_vector.x += -self._PLAYER_MOVE_SPEED

                if self._KEY_CODE_D in keys_pressed:
                    input_move_vector.x += self._PLAYER_MOVE_SPEED

                return input_move_vector.x

            _KEY_CODE_SPACE: int = 32

            _GRAVITY_ACCELERATION: Vector2D = Vector2D(0, 2.5)
            _MAX_VERTICAL_VELOCITY: int = 12

            _vertical_velocity: Vector2D = Vector2D()

            def _get_vertical_velocity(self, keys_pressed: Set[int]) -> float:
                """Method calculates current player's vertical velocity"""
                if (
                        self._KEY_CODE_SPACE in keys_pressed
                        and self._jump_is_available):
                    # Initial jump velocity
                    self._vertical_velocity.y = -25
                    self._jump_is_available = False

                elif (self._vertical_velocity.y + self._GRAVITY_ACCELERATION.y
                      < self._MAX_VERTICAL_VELOCITY):
                    self._vertical_velocity.y += self._GRAVITY_ACCELERATION.y

                else:
                    self._vertical_velocity.y = self._MAX_VERTICAL_VELOCITY

                return self._vertical_velocity.y

        _state_updater: StateUpdater
        # _game_objects_spawner: GameObjectsSpawner

        def update_map(self):  # pragma: no cover
            """Main update method that should be invoked from the game loop

            All update methods are here"""
            self._state_updater.update_player_state()

    _gui: GameGUI = GameGUI()
    _map_updater: MapUpdater

    # Not seconds because of possible lags. If lags are presented then all game model
    # will work fine and consistently without leaps that can occur because of seconds
    # counting
    _game_loop_iterations_count: int = 0

    # At the same time one instance of game map can be either in the process of rendering
    # OR updating because of instance modifications in game loop thread. Game map
    # cloning would solve this restriction but it would be expensive and, actually,
    # useless: if some renders or updates are lost OR require too much time -
    # gameplay would be ruined anyway
    _game_map: GameMap

    def start_game(self):  # pragma: no cover
        """Initialize game loop"""
        self._gui.init(self._game_map, self)

        Thread(target=self._game_loop, daemon=True).start()
        # Right here several renderings CANNOT be lost
        self._gui.run_gui_loop()

    @staticmethod
    def _time_alignment():  # pragma: no cover
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

    def _game_loop(self):  # pragma: no cover
        # Game loop is in a daemon thread so it will proceed until gui thread is closed
        while True:
            self._map_updater.update_map()

            self._gui.render()

            self._time_alignment()

            self._game_loop_iterations_count += 1
