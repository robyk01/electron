from .base import Component

class VoltageSource(Component):
    def __init__(self, name, volts, x, y):
        super().__init__(name, x, y)
        self.voltage = volts

    def __repr__(self):
        return f"Voltage {self.name}: {self.voltage}"


class Resistor(Component):
    def __init__(self, name, ohms, x, y):
        super().__init__(name, x, y)
        self.resistance = ohms

    def __repr__(self):
        return f"Resistor {self.name}: {self.resistance}"


class Capacitor(Component):
    def __init__(self, name, farads, x, y):
        super().__init__(name, x, y)
        self.capacitance = farads

    def __repr__(self):
        return f"Capacitor {self.name}: {self.capacitance}F"


class Transistor(Component):
    def __init__(self, name, model_type, x, y):
        super().__init__(name, x, y, pin_count=3)
        self.model_type = model_type

    # transistor pins: 0 - collector, 1 - base, 2 - emitter
    def get_pin_positions(self):
        offset = 20

        if self.rotation == 0:  # Horizontal
            return [
                (self.x - offset, self.y - offset // 2),  
                (self.x, self.y + offset),                 
                (self.x + offset, self.y - offset // 2)    
            ]
        elif self.rotation == 90:  # Rotated 90° clockwise
            return [
                (self.x + offset // 2, self.y - offset),   
                (self.x - offset, self.y),                  
                (self.x + offset // 2, self.y + offset)
            ]
        elif self.rotation == 180:  # Upside down
            return [
                (self.x + offset, self.y + offset // 2),
                (self.x, self.y - offset),                  
                (self.x - offset, self.y + offset // 2)    
            ]
        elif self.rotation == 270:  # Rotated 270°
            return [
                (self.x - offset // 2, self.y + offset),   
                (self.x + offset, self.y),                  
                (self.x - offset // 2, self.y - offset)    
            ]
        
        return []
        

    def __repr__(self):
        return f"Tranzistor {self.name} ({self.model_type})"
    
class Ground(Component):
    def __init__(self, name, x, y):
        super().__init__(name, x, y, pin_count=1)
        self.img_name = "ground.png"

        self.nodes[0] = 0
    
    def get_pin_positions(self):
        return [(self.x, self.y + 20)]
    
    def __repr__(self):
        return f"Ground {self.name}"
    
class LED(Component):
    def __init__(self, name, x, y):
        super().__init__(name, x, y, pin_count=2)
        self.forward_voltage = 2.0  # red led
        self.resistance = 10.0 
    
    def __repr__(self):
        return f"LED {self.name}"