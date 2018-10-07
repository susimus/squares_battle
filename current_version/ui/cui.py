from engine.game_object import GameObject  #  pragma: no cover
from engine.enums import GameObjectType, MoveDirection  #  pragma: no cover
from os import system as os_system  #  pragma: no cover
from platform import system as platform_system  #  pragma: no cover
from time import sleep as time_sleep  #  pragma: no cover


class ConsoleUserInterface:  #  pragma: no cover
    def __init__(self, game_map):
        if platform_system() == 'Linux':
            self.clear_console = lambda: os_system('clear')
        elif platform_system() == 'Windows':
            self.clear_console = lambda: os_system('cls')
        else:
            raise OSError("Operational system is not supported for program!")
    
        self.game_map = \
            [[] for x in range(game_map[0].net_dimensions[0])]
        for x in range(game_map[0].net_dimensions[0]):
            self.game_map[x] = \
                [[] for y in range(game_map[0].net_dimensions[1])]
        
        for i in range(1, len(game_map)):
            obj_position = game_map[i].current_position
            
            self.game_map[obj_position[0]][obj_position[1]] = [game_map[i]]

    #  def add_game_object(self, game_object)

    def draw_map(self):
        self.clear_console()
        for y in range(len(self.game_map[0])):
            for x in range(len(self.game_map)):
                if self.game_map[x][y] == []:
                    print('.', end=' ')
                elif self.game_map[x][y][0].object_type \
                   == GameObjectType.Player:
                    print('*', end=' ')
            print()
        
        time_sleep(0.01 )
            
    def move_object_on_position(self, obj_position, x_modifier, y_modifier):
        self.game_map\
            [obj_position[0] + x_modifier]\
            [obj_position[1] + y_modifier] = \
            [self.game_map[obj_position[0]][obj_position[1]][0]]
        self.game_map[obj_position[0]][obj_position[1]] = []
