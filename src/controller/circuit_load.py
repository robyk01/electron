import json
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

from src.model.circuit import Circuit
from src.model.elements import Resistor, VoltageSource, Capacitor, Transistor
from src.controller.connection import Connection

SCHEMA_VERSION = 1

def _component_to_dict(comp) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "uuid": str(comp.uuid),
        "type": comp.__class__.__name__,
        "name": comp.name,
        "x": comp.x,
        "y": comp.y,
        "rotation": getattr(comp, "rotation", 0),
    }

    # type-specific
    if isinstance(comp, Resistor):
        data["resistance"] = comp.resistance
    elif isinstance(comp, VoltageSource):
        data["voltage"] = comp.voltage
    elif isinstance(comp, Capacitor):
        data["capacitance"] = comp.capacitance
    elif isinstance(comp, Transistor):
        data["model_type"] = comp.model_type

    return data

def _wire_to_dict(wire) -> Dict[str, Any]:
    comp1, pin1, comp2, pin2 = wire
    return {
        "a": str(comp1.uuid),
        "a_pin": pin1,
        "b": str(comp2.uuid),
        "b_pin": pin2,
    }

def save_circuit(path: str, circuit: Circuit, connection: Connection) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "components": [_component_to_dict(c) for c in circuit.components],
        "wires": [_wire_to_dict(w) for w in connection.wires],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def load_circuit(path: str) -> Tuple[Circuit, Connection]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    circuit = Circuit()
    connection = Connection(circuit)

    # 1) recreate components
    uuid_map: Dict[str, Any] = {}
    for c in payload.get("components", []):
        ctype = c.get("type")
        name = c.get("name")
        x = c.get("x", 0)
        y = c.get("y", 0)

        comp = None
        if ctype == "Resistor":
            comp = Resistor(name, c.get("resistance", 1000), x, y)
            comp.img_name = "rezistor.png"
        elif ctype == "VoltageSource":
            comp = VoltageSource(name, c.get("voltage", 9), x, y)
            comp.img_name = "baterie.png"
        elif ctype == "Capacitor":
            comp = Capacitor(name, c.get("capacitance", 1e-6), x, y)
            comp.img_name = "capacitor.png"
        elif ctype == "Transistor":
            comp = Transistor(name, c.get("model_type", "NPN"), x, y)
            comp.img_name = "tranzistor.png"
        else:
            continue

        comp.rotation = c.get("rotation", 0)

        # restore rect same way you do in main when placing
        import pygame
        comp.rect = pygame.Rect(x - 20, y - 20, 40, 40)

        circuit.add_component(comp)
        uuid_map[c.get("uuid")] = comp

    # recreate wires 
    connection.wires = []
    connection.node_counter = 1
    circuit.active_nodes = set()

    for w in payload.get("wires", []):
        a = uuid_map.get(w.get("a"))
        b = uuid_map.get(w.get("b"))
        if a is None or b is None:
            continue
        a_pin = int(w.get("a_pin", 0))
        b_pin = int(w.get("b_pin", 0))

        ok = connection.create_connection(a, a_pin, b, b_pin)
        if ok:
            connection.wires.append((a, a_pin, b, b_pin))

    if circuit.active_nodes:
        connection.node_counter = max(circuit.active_nodes) + 1

    return circuit, connection