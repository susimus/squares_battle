class GameObject:
    def __init__(self,
                 object_type,
                 movable, 
                 net_dimensions, 
                 current_position,
                 cell_size):
        self.object_type = object_type
        self.movable = movable
        self.net_dimensions = net_dimensions
        self.current_position = current_position
        self.cell_size = cell_size
