from time import (
    time as current_time_in_seconds,
    sleep as time_sleep)
from threading import Thread
from typing import Set, Callable

from maps import GameMap
from user_interface.game_ui import GameGUI, EventListener
from engine.game_objects import *
from engine.collisions_processor import (
    CollisionsProcessor, Collision, GameEvent)
from engine import ApplicationException


class GameEngine(EventListener):
    """All game logic processes here

    If game map without movable objects is given then engine spawns one
    [Player] instance on (0, 0) coordinates
    """
    class MapUpdater:
        """All map state updating logic is here
        """
        class StateUpdater:
            """All game objects state updating is here

            NOW there is only one main instance of [Player] that can move
            and do stuff
            """
            _KEY_CODE_A: int = 65
            _KEY_CODE_D: int = 68
            _KEY_CODE_SPACE: int = 32

            # Constant move speed with global multiplier
            _PLAYER_MOVE_SPEED: int = 6
            _PMS_gb_multiplier: float

            _GRAVITY_ACCELERATION: Vector2D = Vector2D(0, 2.5)
            _MAX_VERTICAL_VELOCITY: float = 12

            # Constant initial jump velocity with global multiplier
            _INITIAL_JUMP_VELOCITY: float = -25
            _IJV_gb_multiplier: float

            _collisions_processor: CollisionsProcessor

            _game_map: GameMap
            _keys_pressed: Set[int]

            # If so then main [Player] can jump
            # Optimization: When main [Player] is on the ground then no
            #  collisions with the ground should be initiated
            _player_is_on_the_ground: bool

            _vertical_velocity: float

            _get_game_loop_iterations_count: Callable[[], int]

            def __init__(self, game_engine: 'GameEngine'):
                self._game_map = game_engine._game_map
                self._keys_pressed = game_engine._keys_pressed
                self._collisions_processor = CollisionsProcessor(
                    game_engine._game_map)

                self._player_is_on_the_ground = False
                self._vertical_velocity = 0

                self._PMS_gb_multiplier = 1
                self._IJV_gb_multiplier = 1

                self._get_game_loop_iterations_count = (
                    game_engine.get_game_loop_iterations_count)

            def update_movable_objects_states(self):
                self._refresh_global_movement_multipliers()

                for movable_object in self._game_map.movable_objects:
                    if isinstance(movable_object, Player):
                        self._update_player_state(movable_object)

                    else:
                        GameEngineException(
                            "While processing [update_movable_objects_states] "
                            "method, got [movable_object] with unknown type: "
                            + movable_object.__class__.__name__)

            def _refresh_global_movement_multipliers(self):
                self._PMS_gb_multiplier = self._IJV_gb_multiplier = 1

            def _update_player_state(self, player: Player):  # pragma: no cover
                self._check_player_buffs(player)

                # Copy in case if '_keys_pressed' will be modified during check
                keys_pressed_copy: Set[int] = set(self._keys_pressed)
                player_move_vector: Vector2D = Vector2D(0, 0)

                player_move_vector.x += self._get_horizontal_velocity(
                    keys_pressed_copy)
                player_move_vector.y += self._get_vertical_velocity(
                    keys_pressed_copy)

                if player_move_vector.x != 0 or player_move_vector.y != 0:
                    player_collisions: List[Collision] = (
                        self._collisions_processor.get_collisions(
                            player, player_move_vector))

                    for collision in player_collisions:
                        self._process_player_collision(
                            player, collision, player_move_vector)

                    if player_move_vector.y != 0:
                        self._player_is_on_the_ground = False

                    player.location += player_move_vector

            def _process_player_collision(
                    self,
                    player: Player,
                    collision: Collision,
                    player_move_vector: Vector2D):  # pragma: no cover
                if collision.collided_object is None:
                    if (collision.game_event
                            is GameEvent.PLAYER_BORDERS_RIGHT):
                        player_move_vector.x = 0
                        player.location.x = (
                            self._game_map.game_field_size.x
                            # '+ 1' for closest to border drawing
                            - PaintingConst.PLAYER_SIDE_LENGTH + 1)

                    elif (collision.game_event
                          is GameEvent.PLAYER_BORDERS_LEFT):
                        player_move_vector.x = 0
                        player.location.x = 0

                    elif (collision.game_event
                          is GameEvent.PLAYER_BORDERS_BOTTOM):
                        player_move_vector.y = 0

                        # Teleport Player close to game borders
                        player.location.y = (
                            self._game_map.game_field_size.y
                            - PaintingConst.PLAYER_SIDE_LENGTH + 1)

                        self._player_is_on_the_ground = True

                    elif (collision.game_event
                          is GameEvent.PLAYER_BORDERS_TOP):
                        player_move_vector.y = 0
                        player.location.y = 0

                    else:
                        raise PlayerCollisionsSwitchError(
                            '[collided_object] is [None], [game_event] is '
                            'unknown',
                            collision.game_event.name)

                elif isinstance(collision.collided_object, AbstractBuff):
                    if collision.game_event is GameEvent.PLAYER_BUFF:
                        collision.collided_object.capture_this_buff(
                            self._get_game_loop_iterations_count(),
                            player)
                    else:
                        raise PlayerCollisionsSwitchError(
                            '[collided_object] is instance of [AbstractBuff], '
                            '[game_event] is unknown',
                            collision.game_event.name)

                elif isinstance(collision.collided_object, BasicPlatform):
                    if (collision.game_event
                            is GameEvent.PLAYER_TOP_BASIC_PLATFORM):
                        player_move_vector.y = 0

                        player.location.y = (
                            collision.collided_object.location.y
                            + collision.collided_object.height + 1)

                    elif (collision.game_event
                            is GameEvent.PLAYER_BOTTOM_BASIC_PLATFORM):
                        player_move_vector.y = 0

                        player.location.y = (
                            collision.collided_object.location.y
                            - PaintingConst.PLAYER_SIDE_LENGTH - 1)

                        self._player_is_on_the_ground = True

                    elif (collision.game_event
                            is GameEvent.PLAYER_RIGHT_BASIC_PLATFORM):
                        player_move_vector.x = 0

                        player.location.x = (
                            collision.collided_object.location.x
                            - PaintingConst.PLAYER_SIDE_LENGTH - 1)

                    elif (collision.game_event
                            is GameEvent.PLAYER_LEFT_BASIC_PLATFORM):
                        player_move_vector.x = 0

                        player.location.x = (
                            collision.collided_object.location.x
                            + collision.collided_object.width + 1)

                    else:
                        raise PlayerCollisionsSwitchError(
                            '[collided_object] is instance of [BasicPlatform],'
                            '[game_event] is unknown',
                            collision.game_event.name)

                else:
                    raise PlayerCollisionsSwitchError(
                        "[collided_object] is unknown",
                        collision.collided_object.__class__.__name__)

            def _check_player_buffs(self, player: Player):
                for buff in player.current_buffs:
                    if isinstance(buff, SpeedUpBuff):
                        self._PMS_gb_multiplier = 2

                    elif isinstance(buff, JumpHeightUpBuff):
                        self._IJV_gb_multiplier = 1.5

                    else:
                        raise GameEngineException(
                            "[_check_player_buffs] method got [buff] with "
                            "unknown type: " + buff.__class__.__name__)

            def _get_horizontal_velocity(
                    self, keys_pressed: Set[int]) -> float:
                """Method gets player's current horizontal velocity"""
                input_move_vector: Vector2D = Vector2D(0, 0)

                if self._KEY_CODE_A in keys_pressed:
                    input_move_vector.x += (
                        -self._PLAYER_MOVE_SPEED * self._PMS_gb_multiplier)

                if self._KEY_CODE_D in keys_pressed:
                    input_move_vector.x += (
                        self._PLAYER_MOVE_SPEED * self._PMS_gb_multiplier)

                return input_move_vector.x

            def _get_vertical_velocity(self, keys_pressed: Set[int]) -> float:
                """Method calculates current player's vertical velocity"""
                if (
                        self._KEY_CODE_SPACE not in keys_pressed
                        and self._player_is_on_the_ground):
                    self._vertical_velocity = self._GRAVITY_ACCELERATION.y
                elif (
                        self._KEY_CODE_SPACE in keys_pressed
                        and self._player_is_on_the_ground):
                    self._vertical_velocity = (
                        self._INITIAL_JUMP_VELOCITY * self._IJV_gb_multiplier)
                    self._player_is_on_the_ground = False

                elif (self._vertical_velocity + self._GRAVITY_ACCELERATION.y
                      < self._MAX_VERTICAL_VELOCITY):
                    self._vertical_velocity += self._GRAVITY_ACCELERATION.y

                else:
                    self._vertical_velocity = self._MAX_VERTICAL_VELOCITY

                return self._vertical_velocity

            def update_immovable_objects_states(self):
                for immovable_object in self._game_map.immovable_objects:
                    if isinstance(immovable_object, AbstractBuff):
                        self._update_buff_state(immovable_object)

                    else:
                        GameEngineException(
                            "[update_immovable_objects_states] method got "
                            "[immovable_object] with unknown type: "
                            + immovable_object.__class__.__name__)

            def _update_buff_state(self, buff: AbstractBuff):
                buff.check_buff_expiration(
                    self._get_game_loop_iterations_count())

        # TODO: Implement [GameObjectsSpawner]
        # class GameObjectsSpawner:
        #     """All game objects spawning is here"""
        #     _game_map: GameMap

        _state_updater: StateUpdater
        # _game_objects_spawner: GameObjectsSpawner

        def __init__(self, game_engine: 'GameEngine'):
            self._state_updater = self.StateUpdater(game_engine)

        def update_map(self):  # pragma: no cover
            """Main update method that should be invoked from the game loop

            All update methods are here"""
            # WouldBeBetter: Update interface objects states

            self._state_updater.update_immovable_objects_states()

            self._state_updater.update_movable_objects_states()

    _map_updater: MapUpdater

    _gui: GameGUI

    # All key codes of keys that are currently pressed. Without lock because
    # modifying appears only in 'event listener' methods. In all other places
    # this field is just read
    _keys_pressed: Set[int]

    # Not seconds because of possible lags. If lags are presented then all game
    # model will work fine and consistently without leaps that can occur
    # because of seconds counting
    _game_loop_iterations_count: int

    # At the same time one instance of game map can be either in the process of
    # rendering OR updating because of instance modifications in game loop
    # thread. Game map cloning would solve this restriction but it would be
    # expensive and, actually, useless: if some renders or updates are lost
    # OR require too much time - gameplay would be ruined anyway
    _game_map: GameMap

    def __init__(self, input_game_map: GameMap):
        self._keys_pressed = set()
        self._gui = GameGUI()
        self._game_loop_iterations_count = 0

        self._game_map = input_game_map

        if len(self._game_map.movable_objects) == 0:
            self._game_map.movable_objects.append(Player(Vector2D(0, 0)))

        self._map_updater = self.MapUpdater(self)

    def key_pressed(self, key_code: int):  # pragma: no cover
        """Adds pressed key to 'keysPressed' set

        GUI thread enters this method"""
        self._keys_pressed.add(key_code)

    def key_released(self, key_code: int):  # pragma: no cover
        """Subtracts pressed key from 'keysPressed' set

        GUI thread enters this method"""
        self._keys_pressed.discard(key_code)

    def start_game(self):  # pragma: no cover
        """Initialize game loop"""
        self._gui.init(self._game_map, self)

        Thread(target=self._game_loop, daemon=True).start()
        # Right here several renderings CANNOT be lost
        self._gui.run_gui_loop()

    def _game_loop(self):  # pragma: no cover
        # Game loop is in a daemon thread so it will proceed until user
        # interface thread is closed
        while True:
            self._map_updater.update_map()

            self._gui.render()

            self._time_alignment()

            self._game_loop_iterations_count += 1

    @staticmethod
    def _time_alignment():  # pragma: no cover
        """Time alignment for CPU power saving

        Игра работает в режиме 60 итераций игрового цикла (обновление И рендер
        уровня в одной итерации) в секунду.

        По сути, секунда разбита на 60 частей. Выравнивание происходит таким
        образом, что в начале каждой 1\60 части секунды должна начинаться
        КАЖДАЯ итерация игрового цикла. НЕТ гарантии, что при таком подходе
        не будет потеряна одна из 1\60-ой частей секунды

        Таким образом, каждое обновление уровня происходит с рассчетом ТОЛЬКО
        на текущую 1/60 часть секунды. Это позволяет избавиться от дробных
        величин при модификации позиции движущихся объектов.
        """
        # All time below in milliseconds
        one_iteration_time: int = 1000 // 60
        millis_in_current_second: int = (
            int(current_time_in_seconds() * 1000) % 1000)
        time_sleep(
            (one_iteration_time
             - millis_in_current_second % one_iteration_time)
            / 1000)

    def get_game_loop_iterations_count(self):
        return self._game_loop_iterations_count


class GameEngineException(ApplicationException):
    pass


class PlayerCollisionsSwitchError(GameEngineException):
    pass
