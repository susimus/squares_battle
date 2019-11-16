from unittest import TestCase, main as unittest_main
from typing import List
from os.path import (
    join as os_path_join,
    dirname as os_path_dirname,
    abspath as os_path_abspath)
from os import pardir as os_pardir
from sys import path as sys_path

sys_path.append(os_path_join(
    os_path_dirname(os_path_abspath(__file__)), os_pardir))

from engine.collisions_processor import (
    CollisionsProcessor, Collision, GameEvent, CollisionsProcessorException)
from maps import GameMap
from engine.game_objects import (
    Vector2D, Player, MovableObject, SpeedUpBuff, BasicPlatform)


test_map_1: GameMap = GameMap(
    Vector2D(100, 100),
    [],
    [Player(Vector2D(0, 0))])

test_map_2: GameMap = GameMap(
    Vector2D(100, 100),
    [SpeedUpBuff(Vector2D(50, 50))],
    [Player(Vector2D(0, 0))])

test_map_3: GameMap = GameMap(
    Vector2D(100, 100),
    [BasicPlatform(10, 10, Vector2D(30, 30))],
    [Player(Vector2D(0, 0))])


class ExceptionsTests(TestCase):
    def test_unknown_moving_object_exception(self):
        with self.assertRaises(CollisionsProcessorException) as occurred_exc:
            CollisionsProcessor(test_map_1).get_collisions(
                MovableObject(Vector2D(0, 0)), Vector2D(0, 0))

        assert len(occurred_exc.exception.args) == 1
        assert occurred_exc.exception.args[0] == (
            'While processing [get_collisions] method, got [moving_object] '
            'with unknown type: MovableObject')


class PlayerCollisionsTests(TestCase):
    def test_right_border_collision(self):
        right_border_collision: List[Collision] = (
            CollisionsProcessor(test_map_1).get_collisions(
                test_map_1.movable_objects[0],
                Vector2D(200, 0)))

        self.assertEqual(1, len(right_border_collision))

        assert (right_border_collision[0].game_event
                is GameEvent.PLAYER_BORDERS_RIGHT)
        assert (right_border_collision[0].moving_object
                is test_map_1.movable_objects[0])
        assert right_border_collision[0].collided_object is None

    def test_left_border_collision(self):
        left_border_collision: List[Collision] = (
            CollisionsProcessor(test_map_1).get_collisions(
                test_map_1.movable_objects[0], Vector2D(-200, 0)))

        self.assertEqual(1, len(left_border_collision))

        assert (left_border_collision[0].game_event
                is GameEvent.PLAYER_BORDERS_LEFT)
        assert (left_border_collision[0].moving_object
                is test_map_1.movable_objects[0])
        assert left_border_collision[0].collided_object is None

    def test_top_border_collision(self):
        top_border_collision: List[Collision] = (
            CollisionsProcessor(test_map_1).get_collisions(
                test_map_1.movable_objects[0], Vector2D(0, -200)))

        self.assertEqual(1, len(top_border_collision))

        assert (top_border_collision[0].game_event
                is GameEvent.PLAYER_BORDERS_TOP)
        assert (top_border_collision[0].moving_object
                is test_map_1.movable_objects[0])
        assert top_border_collision[0].collided_object is None

    def test_bottom_border_collision(self):
        bottom_border_collision: List[Collision] = (
            CollisionsProcessor(test_map_1).get_collisions(
                test_map_1.movable_objects[0], Vector2D(0, 200)))

        self.assertEqual(1, len(bottom_border_collision))

        assert (bottom_border_collision[0].game_event
                is GameEvent.PLAYER_BORDERS_BOTTOM)
        assert (bottom_border_collision[0].moving_object
                is test_map_1.movable_objects[0])
        assert bottom_border_collision[0].collided_object is None

    def test_no_borders_collisions(self):
        no_border_collision: List[Collision] = (
            CollisionsProcessor(test_map_1).get_collisions(
                test_map_1.movable_objects[0], Vector2D(0, 10)))

        self.assertEqual(0, len(no_border_collision))

    def test_player_buff_collision(self):
        collisions: List[Collision] = (
            CollisionsProcessor(test_map_2).get_collisions(
                test_map_2.movable_objects[0],
                Vector2D(30, 30)))

        self.assertEqual(1, len(collisions))
        self.assertEqual(GameEvent.PLAYER_BUFF, collisions[0].game_event)
        self.assertEqual(
            test_map_2.immovable_objects[0],
            collisions[0].collided_object)
        self.assertEqual(
            test_map_2.movable_objects[0],
            collisions[0].moving_object)

    def test_player_basic_platform_collision(self):
        collisions: List[Collision] = (
            CollisionsProcessor(test_map_3).get_collisions(
                test_map_3.movable_objects[0],
                Vector2D(20, 20)))

        self.assertEqual(1, len(collisions))
        self.assertEqual(
            GameEvent.PLAYER_TOP_BASIC_PLATFORM, collisions[0].game_event)
        self.assertEqual(
            test_map_3.movable_objects[0], collisions[0].moving_object)
        self.assertEqual(
            test_map_3.immovable_objects[0], collisions[0].collided_object)


if __name__ == '__main__':
    unittest_main()
