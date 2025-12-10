from .base import Component
from elements import VoltageSource, Resistor

class Circuit:
    def __init__(self):
        parts = []

    def add_part(self, part: Component):
        self.parts.append(part) 
