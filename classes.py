class Bullet:
    
    def __init__(self, dimensions, direction):
        self.dimensions=dimensions
        self.direction=direction
    
    def get_direction(self):
        return self.direction
    
    def get_dimensions(self):
        return self.dimensions