import uuid

class Component:
    def __init__(self, name, x, y,  pin_count = 2):
        self.uuid = uuid.uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.nodes = [None] * pin_count
    
    # return the visual positions of the pins (0 - left, 1 - right)
    def get_pin_positions(self):
        if len(self.nodes) == 2:
            return [
                (self.x - 20, self.y), # pin 0
                (self.x + 20, self.y)  # pin 1
            ]
        
        # TODO: add transistor function (3 pins)
        return []
    
    # checks if mouse hovers a pin
    # returns the pin's index or None
    def get_pin_at_position(self, mx, my, threshold=15):
        for i, (px, py) in enumerate(self.get_pin_positions()):
            distance = (mx - px) ** 2 + (my - py) ** 2
            if distance < threshold**2:
                return i
            
        return None


    def __repr__(self):
        return f"<{self.name}>"


