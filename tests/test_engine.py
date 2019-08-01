from unittest import (
    TestCase,
    main as unittest_main)

from engine.engine import GameVector


class GameVectorTest(TestCase):
    @staticmethod
    def test_adding():
        vector_1 = GameVector(1, 2)
        vector_2 = GameVector(3, 4)

        assert vector_1 + vector_2 == GameVector(4, 6)


if __name__ == "__main__":
    unittest_main()
