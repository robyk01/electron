import uuid


class Component:
    def __init__(self, name, x, y, pin_count=2):
        self.uuid = uuid.uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.nodes = [None] * pin_count
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360
        print(f"{self.name} rotated to {self.rotation} degrees")

    def get_pin_positions(self):
        offset = 20  # Distanta de la centru la pin
        if self.rotation == 0:
            return [(self.x - offset, self.y), (self.x + offset, self.y)]

        elif self.rotation == 90:
            return [(self.x, self.y + offset), (self.x, self.y - offset)]

        elif self.rotation == 180:
            return [(self.x + offset, self.y), (self.x - offset, self.y)]

        elif self.rotation == 270:
            return [(self.x, self.y - offset), (self.x, self.y + offset)]
        return []

    def get_pin_at_position(self, mx, my, threshold=15):
        for i, (px, py) in enumerate(self.get_pin_positions()):
            distance = (mx - px) ** 2 + (my - py) ** 2
            if distance < threshold ** 2:
                return i

        return None

    def __repr__(self):
        return f"<{self.name}>"