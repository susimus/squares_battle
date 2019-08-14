from engine.collisions_processor import CollisionsProcessor, Collision, GameEvent
from maps.maps_processor import GameMap
from engine.game_objects import Vector2D, Player, GameObject

from unittest import TestCase
from typing import List


only_player_small_map: GameMap = GameMap(Vector2D(100, 100), Player())


class ExceptionsTests(TestCase):
    def test_unknown_moving_object_exception(self):
        with self.assertRaises(ValueError) as occurred_exc:
            CollisionsProcessor(only_player_small_map).get_collisions(
                GameObject(), Vector2D())

        assert len(occurred_exc.exception.args) == 1
        assert occurred_exc.exception.args[0] == (
            'Got unknown class of [moving_object]: GameObject')


class PlayerCollisionsTests(TestCase):
    _collisions_processor: CollisionsProcessor = CollisionsProcessor(
        only_player_small_map)

    def test_right_border_collision(self):
        right_border_collision: List[Collision] = (
            self._collisions_processor.get_collisions(
                only_player_small_map.player, Vector2D(200, 0)))

        assert len(right_border_collision) == 1

        assert right_border_collision[0].game_event is GameEvent.PLAYER_IS_OUT_RIGHT
        assert right_border_collision[0].moving_object is only_player_small_map.player
        assert right_border_collision[0].collided_object is None

    def test_left_border_collision(self):
        left_border_collision: List[Collision] = (
            self._collisions_processor.get_collisions(
                only_player_small_map.player, Vector2D(-200, 0)))

        assert len(left_border_collision) == 1

        assert left_border_collision[0].game_event is GameEvent.PLAYER_IS_OUT_LEFT
        assert left_border_collision[0].moving_object is only_player_small_map.player
        assert left_border_collision[0].collided_object is None

    def test_top_border_collision(self):
        top_border_collision: List[Collision] = (
            self._collisions_processor.get_collisions(
                only_player_small_map.player, Vector2D(0, -200)))

        assert len(top_border_collision) == 1

        assert top_border_collision[0].game_event is GameEvent.PLAYER_IS_OUT_TOP
        assert top_border_collision[0].moving_object is only_player_small_map.player
        assert top_border_collision[0].collided_object is None

    def test_bottom_border_collision(self):
        bottom_border_collision: List[Collision] = (
            self._collisions_processor.get_collisions(
                only_player_small_map.player, Vector2D(0, 200)))

        assert len(bottom_border_collision) == 1

        assert bottom_border_collision[0].game_event is GameEvent.PLAYER_IS_OUT_BOTTOM
        assert bottom_border_collision[0].moving_object is only_player_small_map.player
        assert bottom_border_collision[0].collided_object is None

    def test_no_borders_collisions(self):
        no_border_collision: List[Collision] = (
            self._collisions_processor.get_collisions(
                only_player_small_map.player, Vector2D(0, 10)))

        assert len(no_border_collision) == 0
