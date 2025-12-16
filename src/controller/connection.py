
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
    
    
