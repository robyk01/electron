from .base import Component
from .elements import VoltageSource, Resistor

class Circuit:
    def __init__(self):
        self.components = []

    def add_component(self, part: Component):
        self.components.append(part) 
        print(f"Am adaugat componenta: {part}")

    def get_component(self):
        return self.components
