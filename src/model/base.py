import uuid

class Component:
    def __init__(self, name, x, y,  pin_count = 2):
        self.uuid = uuid.uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.nodes = [None] * pin_count
    
    def __repr__(self):
        return f"<{self.name}>"


