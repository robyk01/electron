from src.model.circuit import Circuit
from src.model.elements import Resistor, VoltageSource
from src.model.solver import Solver

circuit = Circuit()

battery = VoltageSource("V1", 10, 0, 0)
r1 = Resistor("R1", 100, 0, 0)
r2 = Resistor("R2", 400, 0, 0)

circuit.add_component(battery)
circuit.add_component(r1)
circuit.add_component(r2)

# Baterie: node 0 (ground) - node 1
circuit.connect(battery, 0, 0)  
circuit.connect(battery, 1, 1)  

# R1: node 1 → node 2
circuit.connect(r1, 0, 1)
circuit.connect(r1, 1, 2)

# R2: node 2 → ground
circuit.connect(r2, 0, 2)
circuit.connect(r2, 1, 0)

# Test solver
solver = Solver(circuit)
solver.solve()
