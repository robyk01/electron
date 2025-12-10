from src.model.elements import VoltageSource, Resistor
from src.model.circuit import Circuit

c = Circuit()

v1 = VoltageSource("v1", 9, 0, 0)
c1 = Resistor("r1", 100, 1, 1)

c.add_component(v1)
c.add_component(c1)

print("Circuitul contine:", c.get_component())
