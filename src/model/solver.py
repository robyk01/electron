import numpy as np
from src.model.elements import Resistor, VoltageSource, Transistor, Capacitor
from src.model.circuit import Circuit

class Solver:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    # solve the circuit using Nodal Analysis
    def solve(self):

        voltage_sources = [c for c in self.circuit.components if isinstance(c, VoltageSource)]

        if not voltage_sources:
            return {
                "success": False,
                "error": "Circuit fara sursa de tensiune"
            }
        
        # DEBUG: 
        print("\nDEBUG: Noduri componente inainte de setare ground:")
        for comp in self.circuit.components:
            print(f"  {comp.name}: {comp.nodes}")

        # add ground
        first_battery = voltage_sources[0]

        if first_battery.nodes[0] is None or first_battery.nodes[1] is None:
            return {
                "success": False,
                "error": f"{first_battery.name} nu e complet conectata"
            }
        
        old_ground_node = first_battery.nodes[0]
        first_battery.nodes[0] = 0
        self.circuit.active_nodes.add(0)

        if old_ground_node is not None and old_ground_node != 0:
            for comp in self.circuit.components:
                for i in range(len(comp.nodes)):
                    if comp.nodes[i] == old_ground_node:
                        comp.nodes[i] = 0
            
            self.circuit.active_nodes.discard(old_ground_node)
        
        # DEBUG:
        print("\nDEBUG: Noduri componente dupa setare ground:")
        for comp in self.circuit.components:
            print(f"  {comp.name}: {comp.nodes}")

        nodes = sorted(list(self.circuit.active_nodes - {0}))
        node_count = len(nodes)

        if node_count == 0:
            return {
                "success": False,
                "error": "Nu exista noduri in circuit (doar ground)!"
            }
        
        # mapping for quick access
        node_to_index = {node: i for i, node in enumerate(nodes)}

        transistors = [c for c in self.circuit.components if isinstance(c, Transistor)]
        transistor_states = {t.uuid: False for t in transistors}

        max_iterations = 10
        for iteration in range(max_iterations):

            # conductance matrix
            G_matrix = np.zeros((node_count, node_count))

            for component in self.circuit.components:
                if isinstance(component, Resistor):
                    node1 = component.nodes[0]
                    node2 = component.nodes[1]
                    resistance = component.resistance

                elif isinstance(component, Capacitor):
                    node1 = component.nodes[0]
                    node2 = component.nodes[1]
                    resistance = 1e4

                else: 
                    continue

                if node1 is None or node2 is None:
                    print(f"Avertisment: {component.name} nu e complet conectat!")
                    continue

                # calculate conductance
                conductance = 1.0 / resistance

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

            for t in transistors:
                if t.nodes[0] is None or t.nodes[2] is None:
                    continue

                node_collector = t.nodes[0] # pin 0 = collector
                node_emitter = t.nodes[2] # pin 2 = emitter

                if transistor_states[t.uuid]:
                    R_ce = 10.0 # small resistance if its ON
                else:
                    R_ce = 1e9 # huge resistance if its OFF

                conductance_ce = 1.0 / R_ce

                if node_collector != 0 and node_emitter != 0:
                    idx_c = node_to_index[node_collector]
                    idx_e = node_to_index[node_emitter]

                    G_matrix[idx_c, idx_c] += conductance_ce
                    G_matrix[idx_e, idx_e] += conductance_ce
                    G_matrix[idx_c, idx_e] -= conductance_ce
                    G_matrix[idx_e, idx_c] -= conductance_ce

                elif node_collector == 0 and node_emitter != 0:
                    idx_e = node_to_index[node_emitter]

                    G_matrix[idx_e, idx_e] += conductance_ce

                elif node_collector != 0 and node_emitter == 0:
                    idx_c = node_to_index[node_collector]

                    G_matrix[idx_c, idx_c] += conductance_ce
            
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
                return {
                    "success": False,
                    "error": "Sistemul nu poate fi rezolvat (matrice singulara)"
                }
            
            print("\n--- Soluția V (tensiuni noduri) ---")
            print(V_solution)

            # save nodes tension
            node_voltages = {0: 0.0}
            for i, node_id in enumerate(nodes):
                node_voltages[node_id] = V_solution[i]


            print("\n--- Tensiuni noduri ---")
            for node_id, voltage in sorted(node_voltages.items()):
                print(f"Node {node_id}: {voltage:.3f} V")

            changed = False
            for t in transistors:
                if t.nodes[1] is None or t.nodes[2] is None:
                    continue

                node_base = t.nodes[1]
                node_emitter = t.nodes[2]

                V_base = node_voltages.get(node_base, 0.0)
                V_emitter = node_voltages.get(node_emitter, 0.0)

                # NPN transistor: ON if V_base > V_emitter + 0.7
                new_state = (V_base - V_emitter) > 0.7

                if new_state != transistor_states[t.uuid]:
                    transistor_states[t.uuid] = new_state
                    changed = True

            if not changed:
                print(f"Convergenta dupa {iteration + 1} iteratii")
                break

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
                node_neg = component.nodes[0]

                if node_pos is None or node_neg is None:
                    continue

                total_current = 0.0
                for other_comp in self.circuit.components:
                    if other_comp == component:
                            continue
                    
                    if isinstance(other_comp, Resistor):
                        node1 = other_comp.nodes[0]
                        node2 = other_comp.nodes[1]

                        if node_pos not in [node1, node2]:
                            continue
                        
                        v1 = node_voltages.get(node1, 0)
                        v2 = node_voltages.get(node2, 0)
                        i_res = (v1 - v2) / other_comp.resistance
                        
                        # current flows out of node_pos through nodes[1]
                        if node1 == node_pos:
                            total_current += i_res
                        # current flows in node_pos through nodes[0]
                        else:
                            total_current -= i_res
                
                component_currents[component.uuid] = abs(total_current)
            
            elif isinstance(component, Transistor):
                node_collector = component.nodes[0]
                node_emitter = component.nodes[2]

                if node_collector is None or node_emitter is None:
                    continue
                
                if transistor_states[component.uuid]:
                    # ON: current = (V_c - V_e) / 10Ω
                    v_c = node_voltages.get(node_collector, 0)
                    v_e = node_voltages.get(node_emitter, 0)
                    current = (v_c - v_e) / 10.0
                else:
                    # OFF: no current
                    current = 0.0

                component_currents[component.uuid] = current

            elif isinstance(component, Capacitor):
                node1 = component.nodes[0]
                node2 = component.nodes[1]

                if node1 is None or node2 is None:
                    continue

                v1 = node_voltages[node1]
                v2 = node_voltages[node2]

                # current I = (V1 - V2) / 1e9 
                current = (v1 - v2) / 1e9
                component_currents[component.uuid] = abs(current)


            
        print("\n--- Curenți componente ---")
        for component in self.circuit.components:
            current = component_currents.get(component.uuid, 0)
            print(f"{component.name}: {current:.6f} A")
        
        # print results
        return {
            "node_voltages": node_voltages,
            "component_currents": component_currents,
            "transistor_states": transistor_states,
            "success": True
        }