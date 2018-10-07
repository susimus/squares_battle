from engine.enums import MoveDirection


def get_x_y_modifiers(move_direction):
    x_modifier = 0
    y_modifier = 0
    if move_direction == MoveDirection.Right:
        x_modifier = 1
    elif move_direction == MoveDirection.Down:
        y_modifier = 1
    elif move_direction == MoveDirection.Left:
        x_modifier = -1
    elif move_direction == MoveDirection.Up:
        y_modifier = -1
    else:
        raise ValueError("Helper function got not a direction. "
                         "Gotten: " 
                         + str(move_direction))
    return x_modifier, y_modifier
