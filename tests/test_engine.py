from unittest import TestCase, main as unittest_main
from os.path import (
    join as os_path_join,
    dirname as os_path_dirname,
    abspath as os_path_abspath)
from os import pardir as os_pardir
from sys import path as sys_path

sys_path.append(os_path_join(
    os_path_dirname(os_path_abspath(__file__)), os_pardir))

from engine.game_objects import Vector2D
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


class GameObjectsSpawnerTests(TestCase):
    _game_objects_spawner: GameEngine._GameObjectsSpawner

if __name__ == '__main__':
    unittest_main()
