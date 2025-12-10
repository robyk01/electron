import uuid

class Component:
    def __init__(self, name, x, y):
        self.uuid = uuid.uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.nodes = []
    
    def __repr__(self):
        return f"<{self.name}>"


