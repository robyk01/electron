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

        for component in self.circuit.components:
            if isinstance(component, VoltageSource):
                node_pos = component.nodes[1]
                node_neg = component.nodes[0]

                if node_pos is None or node_neg is None:
                    print(f"Avertisment: {component.name} nu e complet conectat!")
                    continue

                if node_pos != 0:
                    idx = node_to_index[node_pos]
                    
                    G_matrix[idx, :] = 0
                    G_matrix[idx, idx] = 1
                    I_vector[idx] = component.voltage

        print("\n--- Matricea G (după surse) ---")
        print(G_matrix)
        print("\n--- Vectorul I ---")
        print(I_vector)

        # solve the system G * V = I
        try:
            V_solution = np.linalg.solve(G_matrix, I_vector)
        except np.linalg.LinAlgError:
            print("Eroare: Sistemul nu poate fi rezolvat!")
            return None
        
        print("\n--- Soluția V (tensiuni noduri) ---")
        print(V_solution)

        # save nodes tension
        node_voltages = {}
        for i, node_id in enumerate(nodes):
            node_voltages[node_id] = V_solution[i]

        # ground node
        node_voltages[0] = 0.0

        print("\n--- Tensiuni noduri ---")
        for node_id, voltage in sorted(node_voltages.items()):
            print(f"Node {node_id}: {voltage:.3f} V")

        # calc current for each component
        component_currents = {}

        for component in self.circuit.components:
            if isinstance(component, Resistor):
                node1 = component.nodes[0]
                node2 = component.nodes[1]

                if node1 is None or node2 is None:
                    continue

                v1 = node_voltages[node1]
                v2 = node_voltages[node2]

                # current I = (V1 - V2) / R (Ohm's Law)
                current = (v1 - v2) / component.resistance
                component_currents[component.uuid] = current

            # for battery, the current is the sum of currents from the positive node (KCL)
            elif isinstance(component, VoltageSource):
                node_pos = component.nodes[1]

                if node_pos is None:
                    continue

                total_current = 0.0
                for other_comp in self.circuit.components:
                    if isinstance(other_comp, Resistor):
                        if other_comp.nodes[0] == node_pos:
                            v1 = node_voltages[node_pos]
                            v2 = node_voltages[other_comp.nodes[1]]
                            total_current += (v1 - v2) / other_comp.resistance
                        elif other_comp.nodes[1] == node_pos:
                            v1 = node_voltages[other_comp.nodes[0]]
                            v2 = node_voltages[node_pos]
                            total_current += (v1 - v2) / other_comp.resistance
                
                component_currents[component.uuid] = total_current
            
        print("\n--- Curenți componente ---")
        for component in self.circuit.components:
            current = component_currents.get(component.uuid, 0)
            print(f"{component.name}: {current:.6f} A")
        
        # print results
        return {
            "node_voltages": node_voltages,
            "component_currents": component_currents,
            "success": True
        }