from unittest import TestCase, main as unittest_main
from os.path import (
    join as os_path_join,
    dirname as os_path_dirname,
    abspath as os_path_abspath)
from os import pardir as os_pardir
from sys import path as sys_path
from math import sqrt
from enum import Enum

sys_path.append(os_path_join(
    os_path_dirname(os_path_abspath(__file__)), os_pardir))

from engine.game_objects import *
from engine.engine import GameEngine
from maps import GameMap


class StateUpdaterTests(TestCase):
    _state_updater: GameEngine._StateUpdater = GameEngine._StateUpdater(
            GameEngine(GameMap(Vector2D(100, 100), [], [])))

    def test_velocity_to_the_left(self):
        self.assertEqual(
            -self._state_updater._PLAYER_MOVE_SPEED,
            self._state_updater._get_horizontal_velocity(
                {self._state_updater._KEY_CODE_A}))

    def test_velocity_to_the_right(self):
        self.assertEqual(
            self._state_updater._PLAYER_MOVE_SPEED,
            self._state_updater._get_horizontal_velocity(
                {self._state_updater._KEY_CODE_D}))

    def test_no_horizontal_velocity_with_both_keys_pressed(self):
        assert (self._state_updater._get_horizontal_velocity(
            {self._state_updater._KEY_CODE_A,
             self._state_updater._KEY_CODE_D}) == 0)

    def test_no_horizontal_velocity_with_no_keys_pressed(self):
        assert self._state_updater._get_horizontal_velocity(set()) == 0

    def test_initial_jump_velocity(self):
        self._state_updater._player_is_on_the_ground = True

        assert self._state_updater._get_vertical_velocity(
            {self._state_updater._KEY_CODE_SPACE}) == (
                self._state_updater._INITIAL_JUMP_VELOCITY)

    def test_gravity_acceleration(self):
        assert self._state_updater._get_vertical_velocity(set()) == (
            self._state_updater._GRAVITY_ACCELERATION.y)

    def test_max_vertical_velocity(self):
        self._state_updater._vertical_velocity = 100

        assert self._state_updater._get_vertical_velocity(set()) == 12

    def test_buffs_processing(self):
        # noinspection PyTypeChecker
        player: Player = self._state_updater._game_map.movable_objects[0]

        JumpHeightUpBuff(Vector2D(0, 0)).capture_this_buff(
            0,
            player)
        SpeedUpBuff(Vector2D(0, 0)).capture_this_buff(
            0,
            player)

        self._state_updater._check_player_buffs(player)

        self.assertEqual(2, self._state_updater._PMS_gb_multiplier)
        self.assertEqual(1.5, self._state_updater._IJV_gb_multiplier)

        player.current_buffs = []

        self._state_updater._PMS_gb_multiplier = 1
        self._state_updater._IJV_gb_multiplier = 1


class GameObjectsSpawnerTests(TestCase):
    _game_objects_spawner: GameEngine._GameObjectsSpawner = (
        GameEngine._GameObjectsSpawner(
            GameEngine(GameMap(Vector2D(100, 100), [], []))))

    def test_player_hand_cursor_unit_vector_getter(self):
        cursor_location: Vector2D = Vector2D(100, 100)

        # Player hand location = [Vector2D(30, 22)]
        # abs_player_hand_location: Vector2D = Vector2D(30, 22)

        non_unit_vector: Vector2D = Vector2D(70, 78)
        non_unit_vector_length: float = sqrt(70**2 + 78**2)

        self.assertEqual(
            Vector2D(
                non_unit_vector.x / non_unit_vector_length,
                non_unit_vector.y / non_unit_vector_length),
            self._game_objects_spawner._get_player_hand_cursor_unit_vector(
                cursor_location))

    def test_spawn_player_projectiles(self):
        self.assertEqual(True, self._game_objects_spawner._handgun_can_fire)

        class ButtonStateEnum(Enum):
            ButtonRelease = object()
            ButtonPress = object()

        class MouseEvent:
            type = object()
            x = 0
            y = 0

        self._game_objects_spawner._lmb_event = MouseEvent()

        self._game_objects_spawner._lmb_event.type = (
            ButtonStateEnum.ButtonPress)

        self._game_objects_spawner.spawn_player_projectiles()

        self.assertEqual(False, self._game_objects_spawner._handgun_can_fire)
        self.assertEqual(
            2,
            len(self._game_objects_spawner._game_map.movable_objects))

        self._game_objects_spawner._lmb_event.type = (
            ButtonStateEnum.ButtonRelease)

        self._game_objects_spawner.spawn_player_projectiles()

        self.assertEqual(True, self._game_objects_spawner._handgun_can_fire)


if __name__ == '__main__':
    unittest_main()
