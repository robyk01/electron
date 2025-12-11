import numpy as np
from src.model.elements import Resistor, VoltageSource
from src.model.circuit import Circuit

class Solver:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    # solve the circuit using Nodal Analysis
    def solve(self):
        nodes = sorted(list(self.circuit.active_nodes - {0}))
        node_count = len(nodes)

        if node_count == 0:
            print("Eroare: Nu exista noduri in circuit!")
            return None
        
        # mapping for quick access
        node_to_index = {node: i for i, node in enumerate(nodes)}

        # conductance matrix
        G_matrix = np.zeros((node_count, node_count))

        for component in self.circuit.components:
            if isinstance(component, Resistor):
                node1 = component.nodes[0]
                node2 = component.nodes[1]

                if node1 is None or node2 is None:
                    print(f"Avertisment: {component.name} nu e complet conectat!")
                    continue

                # calculate conductance
                conductance = 1.0 / component.resistance

                if node1 != 0 and node2 != 0:
                    idx1 = node_to_index[node1]
                    idx2 = node_to_index[node2]

                    G_matrix[idx1, idx1] += conductance
                    G_matrix[idx2, idx2] += conductance

                    G_matrix[idx1, idx2] -= conductance
                    G_matrix[idx2, idx1] -= conductance

                elif node1 == 0 and node2 != 0:
                    idx2 = node_to_index[node2]
                    G_matrix[idx2, idx2] += conductance

                elif node1 != 0 and node2 == 0:
                    idx1 = node_to_index[node1]
                    G_matrix[idx1, idx1] += conductance
        
        print("\n--- Matricea G (conductanta) ---")
        print(G_matrix)
        print(f"Noduri: {nodes}")

        # intensity vector
        I_vector = np.zeros(node_count)
        