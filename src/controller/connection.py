from src.model.base import Component
from src.model.circuit import Circuit

# manages the connections between components
class Connection:
    def __init__(self, circuit):
        self.circuit = circuit

        self.wire_mode = False

        # selection for first click
        self.wire_start_component = None
        self.wire_start_pin = None

        # ground is node 0
        self.node_counter = 1

        self.wires = []

    # activates/deactivates wire mode by pressing W
    def toggle_wire_mode(self):
        self.wire_mode = not self.wire_mode

        if self.wire_mode is False:
            self.wire_start_component = None
            self.wire_start_pin = None
            print("Wire mode: OFF")
        else:
            print('Wire mode: ON')

        return self.wire_mode
    
    # searches for pin and component at mouse coordinates
    def find_pin_at_position(self, mx, my):
        for comp in self.circuit.components:
            pin_index = comp.get_pin_at_position(mx, my)

            if pin_index is not None:
                return comp, pin_index
            
        return None, None
    
    # handles clicks in wire mode
    def handle_click(self, mx, my):
        if self.wire_mode == False:
            return None
        
        # find clicked component and pin
        clicked_comp, clicked_pin = self.find_pin_at_position(mx, my)

        if clicked_comp is None:
            return None
        
        # first click
        if self.wire_start_component is None:
            self.wire_start_component = clicked_comp
            self.wire_start_pin = clicked_pin

            print(f"Wire start: {clicked_comp.name} pin {clicked_pin}")
            return "wire_started"
        
        # second click
        else:
            # if its the same component and click we reset
            if clicked_comp == self.wire_start_component and clicked_pin == self.wire_start_pin:
                self.wire_start_component = None
                self.wire_start_pin = None
                return None
            
            # create the connection
            success = self.create_connection(self.wire_start_component, self.wire_start_pin, clicked_comp, clicked_pin)

            if success: 
                self.wires.append((self.wire_start_component, self.wire_start_pin, clicked_comp, clicked_pin))

            # reset for the next connection
            self.wire_start_component = None
            self.wire_start_pin = None

            print('Wire completed!')
            return "wire_completed" if success else "wire_failed"
        
    # create an electric connection between 2 pins
    def create_connection(self, comp1, pin1, comp2, pin2):
        if comp1 == comp2:
            print("Nu poti conecta pinii aceleiasi componente!")
            return False
        
        node1 = comp1.nodes[pin1]
        node2 = comp2.nodes[pin2]

        # both pins are disconnected
        if node1 is None and node2 is None:
            new_node = self.node_counter
            self.node_counter += 1

            self.circuit.connect(comp1, pin1, new_node)
            self.circuit.connect(comp2, pin2, new_node)

            print(f"Created node {new_node}: {comp1.name}[{pin1}] -> {comp2.name}[{pin2}]")
            return True

        # comp1 already connected
        elif node1 is not None and node2 is None:
            self.circuit.connect(comp2, pin2, node1)
            print(f"Connected {comp2.name}[{pin2}] to existing node {node1}")
            return True

        # comp2 already connected
        elif node1 is None and node2 is not None:
            self.circuit.connect(comp1, pin1, node2)
            print(f"Connected {comp1.name}[{pin1}] to existing node {node2}")
            return True

        # both comp connected
        else:
            if node1 == node2:
                print(f"Deja conectate la același nod {node1}")
                return False

    def disconnect_component(self, component):
        new_wires = []
        for wire in self.wires:
            c1, p1, c2, p2 = wire
            # Pastram firul doar daca NU contine componenta noastra
            if c1 != component and c2 != component:
                new_wires.append(wire)
            else:
                print(f"DEBUG: Sters fir legat de {component.name}")

        self.wires = new_wires


    

