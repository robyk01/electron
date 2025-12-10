from .base import Component

class VoltageSource(Component):
    def __init__(self, name, volts):
        super().__init__(name)
        self.volts = volts

class Resistor(Component):
    def __init__(self, name, resistence):
        super().__init__(name)
        self.resistence = resistence