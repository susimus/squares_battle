from typing import Set, Callable
from enum import Enum
from math import sqrt, sin, cos
from threading import Lock
from random import uniform as random_uniform

from maps import GameMap
from engine.game_objects import *
from engine.collisions_processor import (
    CollisionsProcessor, Collision, GameEvent)
from engine import ApplicationException
from user_interface import EventListener


# Improvement: ACTUALLY, GameEngine use EventListener methods ONLY for
#  adding keycodes into [_keys_pressed]. It would be more logical if
#  [_StateUpdater] and [_GameObjectsSpawner] have these interface
#  implemented
class GameEngine(EventListener):
    class _StateUpdater(EventListener):
        # Improvement: Relocate some global vars from here to game
        #  objects' classes. E.g., [_PLAYER_MOVE_SPEED] -> [Player]

        # Improvement: Realize 'space' pressing with [EventListener]
        #  implementation when pressing switches 'space_was_pressed' flag?

        _KEY_CODE_A: int = 65
        _KEY_CODE_D: int = 68
        _KEY_CODE_SPACE: int = 32

        # Improvement: Add lock because 'set' operation below is NOT
        #  atomic! Note that it is NOT needed to pass lock into gui,
        #  because gui already invokes methods here. Right here,
        #  in [EventListener] implementation, lock should be used
        _keys_pressed: Set[int]

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

        # If so then main [Player] can jump
        #
        # Optimization: When [Player] is on the ground then no
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
                game_engine.get_map_updates_count)

        def update_movable_objects_states(self):
            self._refresh_global_movement_multipliers()

            for movable_object in self._game_map.movable_objects:
                if isinstance(movable_object, Player):
                    self._update_player_state(movable_object)

                elif isinstance(movable_object, ProjectileObject):
                    self._update_projectile_state(movable_object)

                else:
                    GameEngineException(
                        "While processing [update_movable_objects_states] "
                        "method, got [movable_object] with unknown type: "
                        + movable_object.__class__.__name__)

        def _update_projectile_state(
                self, projectile: ProjectileObject):  # pragma: no cover
            collisions: List[Collision] = (
                self._collisions_processor.get_collisions(
                    projectile, projectile.moving_vector))

            for collision in collisions:
                self._process_projectile_collision(projectile, collision)

            if not projectile.should_be_despawned:
                projectile.location += projectile.moving_vector

        @staticmethod
        def _process_projectile_collision(
                projectile: ProjectileObject,
                collision: Collision):  # pragma: no cover
            if collision.collided_object is None:
                if collision.game_event is GameEvent.PROJECTILE_IS_OUT:
                    projectile.should_be_despawned = True
                else:
                    raise GameEngineException(
                        '[_process_projectile_collision] switch got '
                        'wrong [collision]',
                        '[collided_object] -> [None]',
                        '(UNKNOWN) [game_event] -> '
                        + '[' + collision.game_event.name + ']')

            else:
                raise GameEngineException(
                    '[_process_projectile_collision] switch got '
                    'wrong [collision]',
                    '(UNKNOWN) [collided_object] -> '
                    + '[' + collision.collided_object.__class__.__name__
                    + ']')

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
                        - Player.SIDE_LENGTH + 1)

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
                        - Player.SIDE_LENGTH + 1)

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
                        - Player.SIDE_LENGTH - 1)

                    self._player_is_on_the_ground = True

                elif (collision.game_event
                        is GameEvent.PLAYER_RIGHT_BASIC_PLATFORM):
                    player_move_vector.x = 0

                    player.location.x = (
                        collision.collided_object.location.x
                        - Player.SIDE_LENGTH - 1)

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

        def update_immovable_objects_states(self):  # pragma: no cover
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

    class _GameObjectsSpawner(EventListener):
        """Spawns AND despawns game objects"""
        class _Weapons(Enum):
            Handgun: int = 1
            MachineGun: int = 2

        _KEY_CODE_1: int = 49
        _KEY_CODE_2: int = 50

        _game_map: GameMap

        _get_game_loop_iterations_count: Callable[[], int]

        # lmb (left mouse button) tkinter event
        _lmb_event: Optional
        _lmb_event_lock: Lock

        _selected_weapon: _Weapons

        # One click = one projectile from handgun
        _handgun_can_fire: bool

        def __init__(self, game_engine: 'GameEngine'):
            self._game_map = game_engine._game_map
            self._get_game_loop_iterations_count = (
                game_engine.get_map_updates_count)

            self._lmb_event_lock = Lock()
            self._lmb_event = None

            self._selected_weapon = self._Weapons.Handgun

            self._handgun_can_fire = True

        def lmb_event_happened(self, event):  # pragma: no cover
            with self._lmb_event_lock:
                self._lmb_event = event

        def key_pressed(self, key_code: int):  # pragma: no cover
            if key_code == self._KEY_CODE_1:
                self._selected_weapon = self._Weapons.Handgun

            elif key_code == self._KEY_CODE_2:
                self._selected_weapon = self._Weapons.MachineGun

        def spawn_player_projectiles(self):
            with self._lmb_event_lock:
                current_lmb_event = self._lmb_event

            if current_lmb_event is not None:
                moving_unit_vector: Vector2D = (
                    self._get_player_hand_cursor_unit_vector(
                        Vector2D(
                            current_lmb_event.x, current_lmb_event.y)))
                spawn_multiplier: float = 20
                spawn_location: Vector2D = Vector2D(
                    self._game_map.movable_objects[0].location.x
                    + Player.HAND_LOCATION.x
                    + moving_unit_vector.x * spawn_multiplier,
                    self._game_map.movable_objects[0].location.y
                    + Player.HAND_LOCATION.y
                    + moving_unit_vector.y * spawn_multiplier)

                if self._selected_weapon is self._Weapons.Handgun:
                    if current_lmb_event.type.name == 'ButtonRelease':
                        self._handgun_can_fire = True

                    elif (current_lmb_event.type.name == 'ButtonPress'
                            and self._handgun_can_fire):
                        moving_vector: Vector2D = Vector2D(
                            moving_unit_vector.x
                            * ProjectileObject.PROJECTILE_SPEED,
                            moving_unit_vector.y
                            * ProjectileObject.PROJECTILE_SPEED)

                        self._game_map.movable_objects.append(
                            HandgunProjectile(
                                moving_vector, spawn_location))

                        self._handgun_can_fire = False

                elif self._selected_weapon is self._Weapons.MachineGun:
                    if (current_lmb_event.type.name
                            in ['ButtonPress', 'Motion']):
                        moving_vector: Vector2D = Vector2D(0, 0)

                        # In radians
                        rotation_angle: float = random_uniform(
                            -MachineGunProjectile.ANGLE_SCATTER_RADIUS,
                            MachineGunProjectile.ANGLE_SCATTER_RADIUS)

                        moving_vector.x = (
                            cos(rotation_angle)
                            * moving_unit_vector.x
                            * ProjectileObject.PROJECTILE_SPEED
                            - sin(rotation_angle)
                            * moving_unit_vector.y
                            * ProjectileObject.PROJECTILE_SPEED)

                        moving_vector.y = (
                            sin(rotation_angle)
                            * moving_unit_vector.x
                            * ProjectileObject.PROJECTILE_SPEED
                            + cos(rotation_angle)
                            * moving_unit_vector.y
                            * ProjectileObject.PROJECTILE_SPEED)

                        self._game_map.movable_objects.append(
                            MachineGunProjectile(
                                moving_vector, spawn_location))

        def _get_player_hand_cursor_unit_vector(
                self, cursor_location: Vector2D) -> Vector2D:
            abs_player_hand_location: Vector2D = (
                self._game_map.movable_objects[0].location
                + Player.HAND_LOCATION)

            non_unit_vector: Vector2D = (
                cursor_location - abs_player_hand_location)
            non_unit_vector_length: float = sqrt(
                non_unit_vector.x ** 2 + non_unit_vector.y ** 2)

            return Vector2D(
                non_unit_vector.x / non_unit_vector_length,
                non_unit_vector.y / non_unit_vector_length)

        def check_movable_objects_for_despawning(self):
            i: int = 0

            while i < len(self._game_map.movable_objects):
                movable_object: MovableObject = (
                    self._game_map.movable_objects[i])

                if movable_object.should_be_despawned:
                    self._game_map.movable_objects.remove(movable_object)
                else:
                    i += 1

    _keys_pressed: Set[int]

    # Not seconds because of possible lags. If lags are presented then all game
    # model will work fine and consistently without leaps that can occur
    # because of seconds counting
    _map_updates_count: int

    # At the same time one instance of game map can be either in the process of
    # rendering OR updating because of instance modifications in game loop
    # thread. Game map cloning would solve this restriction but it would be
    # expensive and, actually, useless: if some renders or updates are lost
    # OR require too much time - gameplay would be ruined anyway
    _game_map: GameMap

    _state_updater: _StateUpdater
    _game_objects_spawner: _GameObjectsSpawner

    def __init__(self, input_game_map: GameMap):
        self._game_loop_iterations_count = 0

        self._keys_pressed = set()
        self._lmb_pressed_event = None

        self._map_updates_count = 0

        self._game_map = input_game_map

        self._state_updater = self._StateUpdater(self)
        self._game_objects_spawner = self._GameObjectsSpawner(self)

        # If game map without movable objects is given then engine spawns
        # player on (0, 0) coordinates
        if len(self._game_map.movable_objects) == 0:
            self._game_map.movable_objects.append(Player(Vector2D(0, 0)))

    def key_pressed(self, key_code: int):  # pragma: no cover
        """Adds pressed key to 'keysPressed' set

        GUI thread invokes this method
        """
        self._keys_pressed.add(key_code)

    def key_released(self, key_code: int):  # pragma: no cover
        """Subtracts pressed key from 'keysPressed' set

        GUI thread invokes this method
        """
        self._keys_pressed.discard(key_code)

    # Now there is only one main instance of [Player] that can move
    # and do stuff! It's always first element in [movable_objects] array
    def update_map(self):  # pragma: no cover
        """Main update method that should be invoked from the gameloop"""
        # Improvement: Is this place optimal for player's projectiles
        #  spawning?
        self._game_objects_spawner.spawn_player_projectiles()

        # Improvement:
        #  self._state_updater.update_interface_objects_states()

        self._state_updater.update_immovable_objects_states()

        self._state_updater.update_movable_objects_states()

        # Improvement: Is this place optimal for deletion checking?
        self._game_objects_spawner.check_movable_objects_for_despawning()

        self._map_updates_count += 1

    def get_event_listeners(self) -> List[EventListener]:
        return [self, self._state_updater, self._game_objects_spawner]

    def get_map_updates_count(self) -> int:
        return self._map_updates_count


class GameEngineException(ApplicationException):
    pass


class PlayerCollisionsSwitchError(GameEngineException):
    pass
