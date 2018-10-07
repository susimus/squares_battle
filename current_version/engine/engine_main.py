from engine.collisions_proc import CollisionsProcessor
from engine.enums import MoveDirection
from engine.helper_funcs import get_x_y_modifiers
from ui.cui import ConsoleUserInterface
from platform import system as platform_system
from msvcrt import kbhit as msvcrt_kbhit
from msvcrt import getch as msvcrt_getch


class GameEngine:
    def __init__(self, game_map):
        self.collisions_proc = CollisionsProcessor(game_map)
        self.moving_objects = []
        for game_object in game_map:
            if game_object.movable:
                self.moving_objects += [game_object]

        self.console_interface = ConsoleUserInterface(game_map)

    def _catch_key(self):
        if platform_system() == 'Linux':
            raise NotImplementedError
        elif platform_system() == 'Windows':
            if msvcrt_kbhit():
                return msvcrt_getch() + msvcrt_getch()
        else:
            raise OSError("Operational system is not supported for program!")

    def start_game(self):
        self.console_interface.draw_map()
        while True:
            catched_key = self._catch_key()
            
            if catched_key == b'\xe0M':
                move_direction = MoveDirection.Right
            elif catched_key == b'\xe0P':
                move_direction = MoveDirection.Down
            elif catched_key == b'\xe0K':
                move_direction = MoveDirection.Left
            elif catched_key == b'\xe0H':
                move_direction = MoveDirection.Up
            else:
                continue

            x_modifier, y_modifier = get_x_y_modifiers(move_direction)
            if self.collisions_proc.object_on_position_moved(
               self.moving_objects[0].current_position, 
               x_modifier, y_modifier):
                self.console_interface.move_object_on_position(
                    self.moving_objects[0].current_position, 
                    x_modifier, y_modifier)
                
                obj_position = self.moving_objects[0].current_position
                self.moving_objects[0].current_position = \
                    (obj_position[0] + x_modifier, 
                     obj_position[1] + y_modifier)
            
            self.console_interface.draw_map()
