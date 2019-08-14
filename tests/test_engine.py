from engine.engine import GameEngine
from maps.maps_processor import GameMap

from unittest import TestCase


class VelocityGettersTests(TestCase):
    _state_updater: GameEngine.MapUpdater.StateUpdater = (
        GameEngine.MapUpdater.StateUpdater(GameMap(), set()))

    def test_velocity_to_the_left(self):
        assert self._state_updater._get_horizontal_velocity(
            {self._state_updater._KEY_CODE_A}) == -self._state_updater._PLAYER_MOVE_SPEED

    def test_velocity_to_the_right(self):
        assert self._state_updater._get_horizontal_velocity(
            {self._state_updater._KEY_CODE_D}) == self._state_updater._PLAYER_MOVE_SPEED

    def test_no_horizontal_velocity_with_both_keys_pressed(self):
        assert self._state_updater._get_horizontal_velocity(
            {self._state_updater._KEY_CODE_A, self._state_updater._KEY_CODE_D}) == 0

    def test_no_horizontal_velocity_with_no_keys_pressed(self):
        assert self._state_updater._get_horizontal_velocity(set()) == 0

    def test_initial_jump_velocity(self):
        self._state_updater._jump_is_available = True

        assert self._state_updater._get_vertical_velocity(
            {self._state_updater._KEY_CODE_SPACE}) == (
                self._state_updater._INITIAL_JUMP_VELOCITY)

    def test_gravity_acceleration(self):
        assert self._state_updater._get_vertical_velocity(set()) == (
            self._state_updater._GRAVITY_ACCELERATION.y)

    def test_max_vertical_velocity(self):
        self._state_updater._vertical_velocity = 100

        assert self._state_updater._get_vertical_velocity(set()) == 12