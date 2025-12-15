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

    def __repr__(self):
        return f"Tranzistor {self.name} ({self.model_type})"