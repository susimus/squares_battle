import pathmagic
from engine.collisions_proc import CollisionsProcessor
from maps.maps_proc import RawMapsContainer
from unittest import TestCase


class TestCollisionsProcessor(TestCase):
    def test_simple_movings(self):
        collisions_proc = CollisionsProcessor(RawMapsContainer.get_map_1())

        assert collisions_proc.object_on_position_moved((0, 0), 0, 1)
        assert not collisions_proc.object_on_position_moved((0, 1), -1, 0)
