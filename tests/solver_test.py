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
results = solver.solve()

print("\n📊 VERIFICARE MANUALA:")
print("Asteptat: V1=10V, V2=8V, I=0.02A")
if results:
    v1 = results["node_voltages"][1]
    v2 = results["node_voltages"][2]
    i_r1 = results["component_currents"][r1.uuid]
    
    assert abs(v1 - 10.0) < 0.001, f"❌ V1 gresit: {v1}"
    assert abs(v2 - 8.0) < 0.001, f"❌ V2 gresit: {v2}"
    assert abs(i_r1 - 0.02) < 0.0001, f"❌ I gresit: {i_r1}"
    
    print("✅ TEST 1 PASSED!")


# parallel circuit test
print("\n" + "="*60)
print("TEST 2: Circuit Paralel")
print("="*60)

circuit2 = Circuit()

battery2 = VoltageSource("V2", 12, 0, 0)
r3 = Resistor("R3", 200, 0, 0)  
r4 = Resistor("R4", 300, 0, 0)  

circuit2.add_component(battery2)
circuit2.add_component(r3)
circuit2.add_component(r4)

# battery: ground → node 1
circuit2.connect(battery2, 0, 0)
circuit2.connect(battery2, 1, 1)

# R3: node 1 → ground 
circuit2.connect(r3, 0, 1)
circuit2.connect(r3, 1, 0)

# R4: node 1 → ground
circuit2.connect(r4, 0, 1)
circuit2.connect(r4, 1, 0)

solver2 = Solver(circuit2)
results2 = solver2.solve()

print("\n📊 VERIFICARE MANUALA:")
print("Circuit: 12V cu R3=200Ω și R4=300Ω in paralel")
print("R_paralel = 1/(1/200 + 1/300) = 120Ω")
print("I_total = 12/120 = 0.1A")
print("I_R3 = 12/200 = 0.06A")
print("I_R4 = 12/300 = 0.04A")

if results2:
    i_r3 = results2["component_currents"][r3.uuid]
    i_r4 = results2["component_currents"][r4.uuid]
    i_battery = results2["component_currents"][battery2.uuid]
    
    assert abs(i_r3 - 0.06) < 0.0001, f"❌ I_R3 gresit: {i_r3}"
    assert abs(i_r4 - 0.04) < 0.0001, f"❌ I_R4 gresit: {i_r4}"
    assert abs(i_battery - 0.1) < 0.0001, f"❌ I_battery gresit: {i_battery}"
    
    print("✅ TEST 2 PASSED!")


# mixed circuit

print("\n" + "="*60)
print("TEST 3: Circuit Mixt (Serie + Paralel)")
print("="*60)

circuit3 = Circuit()

battery3 = VoltageSource("V3", 20, 0, 0)
r5 = Resistor("R5", 100, 0, 0)   # Serie
r6 = Resistor("R6", 200, 0, 0)   # Paralel branch 1
r7 = Resistor("R7", 200, 0, 0)   # Paralel branch 2

circuit3.add_component(battery3)
circuit3.add_component(r5)
circuit3.add_component(r6)
circuit3.add_component(r7)

# battery: ground → node 1
circuit3.connect(battery3, 0, 0)
circuit3.connect(battery3, 1, 1)

# R5 (serie): node 1 → node 2
circuit3.connect(r5, 0, 1)
circuit3.connect(r5, 1, 2)

# R6 (paralel): node 2 → ground
circuit3.connect(r6, 0, 2)
circuit3.connect(r6, 1, 0)

# R7 (paralel): node 2 → ground
circuit3.connect(r7, 0, 2)
circuit3.connect(r7, 1, 0)

solver3 = Solver(circuit3)
results3 = solver3.solve()

print("\n📊 VERIFICARE MANUALA:")
print("R6 || R7 = 100Ω (paralel)")
print("R_total = 100 + 100 = 200Ω")
print("I_total = 20/200 = 0.1A")
print("V_R5 = 0.1 × 100 = 10V")
print("V_paralel = 0.1 × 100 = 10V")
print("I_R6 = I_R7 = 10/200 = 0.05A")

if results3:
    v2 = results3["node_voltages"][2]
    i_total = results3["component_currents"][r5.uuid]
    
    assert abs(v2 - 10.0) < 0.001, f"❌ V2 gresit: {v2}"
    assert abs(i_total - 0.1) < 0.0001, f"❌ I_total gresit: {i_total}"
    
    print("✅ TEST 3 PASSED!")
