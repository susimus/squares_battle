import pathmagic
from engine.collisions_proc import CollisionsProcessor
from maps.maps_proc import RawMapsContainer


class TestCollisionsProcessor():
    def test_simple_moving(self):
        collisions_proc = CollisionsProcessor(RawMapsContainer.get_map_1())
        
        collisions_proc.object_on_position_moved((0, 0), 0, 1)