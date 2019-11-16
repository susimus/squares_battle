from typing import TypeVar
from enum import Enum

from maps import GameMap
from engine.game_objects import *
from engine import ApplicationException


class CollisionsProcessor:
    _game_map: GameMap

    # Result list of collisions in current iteration
    _result_collisions: List['Collision']

    GameObject = TypeVar('GameObject', covariant=True)

    def __init__(self, input_map: GameMap):
        self._game_map = input_map

    def get_collisions(
            self,
            moving_object: MovableObject,
            moving_vector: Vector2D) -> List['Collision']:
        """Main collisions acquiring method

        If there is no collisions then empty list is returned
        """
        self._result_collisions = []

        # Optimization: 'Middle' phase where every two objects' circles
        #  collision is checked. Every game object have its circle that
        #  contains this object. It is needed to compare square of sum of
        #  two radiuses and sum of squares of vector between centers of two
        #  circles. (Not root in second case for more performance)

        # 'Narrow' phase with detailed check
        if isinstance(moving_object, Player):
            self._check_player_collisions(
                moving_object,
                moving_vector,
                # Just all immovable_objects in case of no 'middle' phase
                self._game_map.immovable_objects)

        elif isinstance(moving_object, ProjectileObject):
            self._check_projectile_collisions(
                moving_object,
                moving_vector,
                # Just all immovable_objects in case of no 'middle' phase
                self._game_map.immovable_objects)

        else:
            raise CollisionsProcessorException(
                'While processing [get_collisions] method, '
                'got [moving_object] with unknown type: '
                + moving_object.__class__.__name__)

        return self._result_collisions

    def _check_player_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            potentially_collided_objects: List[ImmovableObject]):
        self._check_player_borders_collisions(
            player, moving_vector)

        for game_object in potentially_collided_objects:
            if game_object is player:
                continue

            elif isinstance(game_object, AbstractBuff):
                self._check_player_buff_collisions(
                    player, moving_vector, game_object)

            elif isinstance(game_object, BasicPlatform):
                self._check_player_basic_platform_collisions(
                    player, moving_vector, game_object)

            else:
                raise CollisionsProcessorException(
                    "While processing [_check_player_collisions] method, "
                    "got [some_object] with unknown type: "
                    + game_object.__class__.__name__)

    def _check_player_borders_collisions(
            self,
            player: Player,
            moving_vector: Vector2D):
        # Horizontal
        if (player.location.x + Player.SIDE_LENGTH
                + moving_vector.x > self._game_map.game_field_size.x):
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_RIGHT, None))

        elif player.location.x + moving_vector.x < 0:
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_LEFT, None))

        # Vertical
        if (player.location.y + Player.SIDE_LENGTH
                + moving_vector.y > self._game_map.game_field_size.y):
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_BOTTOM, None))

        elif player.location.y + moving_vector.y < 0:
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BORDERS_TOP, None))

    def _check_player_buff_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            buff: AbstractBuff):
        player_new_left_border: float = player.location.x + moving_vector.x
        player_new_right_border: float = (
            player.location.x
            + Player.SIDE_LENGTH
            + moving_vector.x)
        player_new_top_border: float = player.location.y + moving_vector.y
        player_new_bottom_border: float = (
            player.location.y
            + Player.SIDE_LENGTH
            + moving_vector.y)

        if (player_new_right_border >= buff.location.x
                and player_new_left_border
                <= buff.location.x + AbstractBuff.SIDE_LENGTH
                and player_new_bottom_border >= buff.location.y
                and player_new_top_border
                <= buff.location.y + AbstractBuff.SIDE_LENGTH
                and not buff.is_charging()):
            self._result_collisions.append(
                Collision(player, GameEvent.PLAYER_BUFF, buff))

    def _check_player_basic_platform_collisions(
            self,
            player: Player,
            moving_vector: Vector2D,
            basic_platform: BasicPlatform):
        player_new_left_border: float = player.location.x + moving_vector.x
        player_new_right_border: float = (
            player.location.x
            + Player.SIDE_LENGTH
            + moving_vector.x)
        player_new_top_border: float = player.location.y + moving_vector.y
        player_new_bottom_border: float = (
            player.location.y
            + Player.SIDE_LENGTH
            + moving_vector.y)

        if (player_new_right_border >= basic_platform.location.x
                and player_new_left_border
                <= basic_platform.location.x + basic_platform.width
                and player_new_bottom_border >= basic_platform.location.y
                and player_new_top_border
                <= basic_platform.location.y + basic_platform.height):
            # Improvement: Do checks below must be with '='?
            if (player.location.y + Player.SIDE_LENGTH
                    <= basic_platform.location.y
                    <= player_new_bottom_border
                    <= basic_platform.location.y + basic_platform.height):
                self._result_collisions.append(
                    Collision(
                        player,
                        GameEvent.PLAYER_BOTTOM_BASIC_PLATFORM,
                        basic_platform))

            elif (basic_platform.location.y <= player_new_top_border
                    <= basic_platform.location.y + basic_platform.height
                    <= player.location.y):
                self._result_collisions.append(
                    Collision(
                        player,
                        GameEvent.PLAYER_TOP_BASIC_PLATFORM,
                        basic_platform))

            elif (player.location.x + Player.SIDE_LENGTH
                    <= basic_platform.location.x <= player_new_right_border
                    <= basic_platform.location.x
                    + basic_platform.width):
                self._result_collisions.append(
                    Collision(
                        player,
                        GameEvent.PLAYER_RIGHT_BASIC_PLATFORM,
                        basic_platform))

            elif (basic_platform.location.x <= player_new_left_border
                    <= basic_platform.location.x + basic_platform.width
                    <= player.location.x):
                self._result_collisions.append(
                    Collision(
                        player,
                        GameEvent.PLAYER_LEFT_BASIC_PLATFORM,
                        basic_platform))
            else:
                # This case fires when basic platform is way too small in
                # comparison with player
                #
                # Improvement: What this case additionally mean?
                min_borders_gap: float = min(
                    abs(player_new_right_border - basic_platform.location.x),
                    abs(player_new_left_border
                        - basic_platform.location.x - basic_platform.width),
                    abs(player_new_bottom_border - basic_platform.location.y),
                    abs(player_new_top_border
                        - basic_platform.location.y - basic_platform.height))

                if (min_borders_gap == player_new_right_border
                        - basic_platform.location.x):
                    self._result_collisions.append(
                        Collision(
                            player,
                            GameEvent.PLAYER_RIGHT_BASIC_PLATFORM,
                            basic_platform))
                elif (min_borders_gap == player_new_left_border
                        - basic_platform.location.x - basic_platform.width):
                    self._result_collisions.append(
                        Collision(
                            player,
                            GameEvent.PLAYER_LEFT_BASIC_PLATFORM,
                            basic_platform))
                elif (min_borders_gap == player_new_bottom_border
                      - basic_platform.location.y):
                    self._result_collisions.append(
                        Collision(
                            player,
                            GameEvent.PLAYER_BOTTOM_BASIC_PLATFORM,
                            basic_platform))
                else:
                    self._result_collisions.append(
                        Collision(
                            player,
                            GameEvent.PLAYER_TOP_BASIC_PLATFORM,
                            basic_platform))

    def _check_projectile_collisions(
            self,
            projectile: ProjectileObject,
            # moving_vector
            _: Vector2D,
            # potentially_collided_objects
            __: List[ImmovableObject]):
        self._check_projectile_borders_collisions(projectile)

    def _check_projectile_borders_collisions(
            self, projectile: ProjectileObject):
        if (isinstance(projectile, HandgunProjectile)
                or isinstance(projectile, MachineGunProjectile)):
            circle_diameter: int = projectile.CIRCLE_DIAMETER
        else:
            raise CollisionsProcessorException(
                '[projectile] has unknown type: '
                + projectile.__class__.__name__)

        if (projectile.location.y + circle_diameter <= 0  # Borders' top
            or projectile.location.y
                >= self._game_map.game_field_size.y  # Borders' bottom
            or projectile.location.x + circle_diameter <= 0  # Borders' left
            or projectile.location.x
                >= self._game_map.game_field_size.x):  # Borders' right
            self._result_collisions.append(
                Collision(projectile, GameEvent.PROJECTILE_IS_OUT, None))

    # Improvement: [_check_circle_projectile_basic_platform_collisions]
    def _check_projectile_basic_platform_collisions(self):
        pass


class Collision:
    # Improvement: Is this field really needed? Game engine always knows
    #  what object was moving when it asks for collisions
    _moving_object: MovableObject

    _game_event: 'GameEvent'

    # May be 'None'. For example, if game object is out of game field's borders
    _collided_object: Optional[GameObject]

    def __init__(
            self,
            input_moving_object: MovableObject,
            input_game_event: 'GameEvent',
            input_collided_object: Optional[GameObject]):
        self._moving_object = input_moving_object
        self._game_event = input_game_event
        self._collided_object = input_collided_object

    @property
    def moving_object(self):
        return self._moving_object

    @property
    def game_event(self):
        return self._game_event

    @property
    def collided_object(self):
        return self._collided_object


class GameEvent(Enum):
    """Enumerates all collision events that can occur

    Event name usually have form:
    {OBJECT1}_{OBJECT2}_{OBJECT2_SIDE}
    OR
    {OBJECT1}_{OBJECT1_SIDE}_{OBJECT2}
    """
    PLAYER_BORDERS_RIGHT = object()
    PLAYER_BORDERS_LEFT = object()
    PLAYER_BORDERS_TOP = object()
    PLAYER_BORDERS_BOTTOM = object()

    PLAYER_RIGHT_BASIC_PLATFORM = object()
    PLAYER_LEFT_BASIC_PLATFORM = object()
    PLAYER_TOP_BASIC_PLATFORM = object()
    PLAYER_BOTTOM_BASIC_PLATFORM = object()

    PLAYER_BUFF = object()

    PROJECTILE_IS_OUT = object()
    # Improvement: PROJECTILE_BASIC_PLATFORM = object()


class CollisionsProcessorException(ApplicationException):
    pass
