from src.model.elements import VoltageSource, Resistor
from src.model.circuit import Circuit

# init circuit
c = Circuit()

# init pieces
v1 = VoltageSource("V_Sus", 10, 0, 0)
r1 = Resistor("R_Stanga", 100, 0, 0)
r2 = Resistor("R_Dreapta", 200, 0, 0)
r3 = Resistor("R_Jos", 300, 0, 0)

# add pieces to circuit
c.add_component(v1)
c.add_component(r1)
c.add_component(r2)
c.add_component(r3)

# connect pieces
CENTRUL = 55
EXTERIOR = 0

# connect minus pin of battery to the circuit and the plus to the table
c.connect(v1, 1, CENTRUL)
c.connect(v1, 0, EXTERIOR) 

# connect the rezistor r1 to the circuit
c.connect(r1, 1, CENTRUL)
c.connect(r1, 0, EXTERIOR)

# connect the rezistor r2 to the circuit
c.connect(r2, 0, CENTRUL)
c.connect(r2, 1, EXTERIOR)

# connect the rezistor r3 to the circuit
c.connect(r3, 0, CENTRUL)
c.connect(r3, 1, EXTERIOR)

c.print_netlist()
