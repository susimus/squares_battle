from engine.enums import MoveDirection


class CollisionsProcessor:
    def __init__(self, game_map):
        self.game_map = \
            [[] for x in range(game_map[0].net_dimensions[0])]
        for x in range(game_map[0].net_dimensions[0]):
            self.game_map[x] = \
                [[] for y in range(game_map[0].net_dimensions[1])]
        
        for i in range(1, len(game_map)):
            obj_position = game_map[i].current_position
            
            self.game_map[obj_position[0]][obj_position[1]] = [game_map[i]]
            
    def object_on_position_moved(self, obj_position, x_modifier, y_modifier):
        if obj_position[0] + x_modifier < 0 \
           or obj_position[0] + x_modifier >= len(self.game_map) \
           or obj_position[1] + y_modifier < 0 \
           or obj_position[1] + y_modifier >= len(self.game_map[0]):
            return False

        self.game_map\
            [obj_position[0] + x_modifier]\
            [obj_position[1] + y_modifier] = \
            [self.game_map[obj_position[0]][obj_position[1]][0]]
        self.game_map[obj_position[0]][obj_position[1]] = []
        
        return True
