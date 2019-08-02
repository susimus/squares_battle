from engine.engine import Vector2D

from unittest import (
    TestCase,
    main as unittest_main)


class Vector2DTest(TestCase):
    @staticmethod
    def test_adding():
        assert Vector2D(1, 2) + Vector2D(3, 4) == Vector2D(4, 6)


if __name__ == "__main__":
    unittest_main()
