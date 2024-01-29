import pennylane as qml
import numpy as np

dev = qml.device('default.qubit', wires=3)


def state_preparation():
    qml.Hadamard(wires=0)
    qml.Rot(0.1, 0.2, 0.3, wires=0)

@qml.qnode(dev)
def state_prep_only():
    state_preparation()
    return qml.state()

def entangle_qubits():

    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1, 2])

def rotate_and_controls():

    qml.CNOT(wires=[0,1])
    qml.Hadamard(wires=0)
    # PERFORM THE CONTROLLED OPERATIONS
    qml.CNOT(wires=[1,2])
    qml.CZ(wires=[0,2])


@qml.qnode(dev)
def teleportation():

    state_preparation()
    qml.Snapshot()
    entangle_qubits()
    rotate_and_controls()
    # RETURN THE STATE
    return qml.state()

def extract_qubit_state(input_state):

    return qml.probs(wires=2)


# Print the extracted state after teleportation
full_state = teleportation()
print(extract_qubit_state(full_state))
