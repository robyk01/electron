import numpy as np
from src.model.elements import Resistor, VoltageSource
from src.model.circuit import Circuit

class Solver:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def solver(self):
        nodes = sorted(list(self.circuit.active_nodes - {0}))
        node_count = len(nodes)

        G_matrix = np.zeros((node_count, node_count))