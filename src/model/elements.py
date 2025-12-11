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