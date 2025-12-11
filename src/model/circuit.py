from .base import Component
from .elements import VoltageSource, Resistor

class Circuit:
    def __init__(self):
        self.components = []
        self.active_nodes = set()

    def add_component(self, part: Component):
        self.components.append(part) 
        print(f"Am adaugat componenta: {part}")

    def get_component(self):
        return self.components
    
    def connect(self, component: Component, pin_index: int, node_id: int):
        if pin_index >= len(component.nodes):
            print(f"Componenta {component} nu are pinul {pin_index}")
            return
        
        component.nodes[pin_index] = node_id
        self.active_nodes.add(node_id)

    def print_netlist(self):
        print("\n--- STAREA CIRCUITULUI ---")
        print(f"Noduri active: {self.active_nodes}")
        for comp in self.components:
            print(f"{comp.name} \t Pini conectati la {comp.nodes} \t Valoare: {getattr(comp, 'voltage', getattr(comp, 'resistance', ''))}")
    
