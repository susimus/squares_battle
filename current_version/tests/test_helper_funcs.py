from engine.enums import MoveDirection
from engine.helper_funcs import *
from unittest import TestCase


class TestHelperFuncs(TestCase):
    def test_get_x_y_modifiers(self):
        assert get_x_y_modifiers(MoveDirection.Right) == (1, 0)
        assert get_x_y_modifiers(MoveDirection.Down) == (0, 1)
        assert get_x_y_modifiers(MoveDirection.Left) == (-1, 0)
        assert get_x_y_modifiers(MoveDirection.Up) == (0, -1)
        try:
            assert get_x_y_modifiers("123")
        except ValueError as _error:
            assert str(_error) == "Helper function got not a direction. "\
                                  "Gotten: 123"
