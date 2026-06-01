import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Define the harmonic scaling ratios
phi = (np.sqrt(5) - 1) / 2  # The Golden Ratio conjugate (0.618...)
rational_ratio = 0.5        # A standard rational phase-lock (1/2)

num_qubits = 5
iterations = 15           # Number of continuous fluid folding cycles
turbulence_factor = 0.15  # The amplitude of kinetic drag applied per cycle

def build_fluid_folding_circuit(ratio, qubits, steps, turbulence):
    qc = QuantumCircuit(qubits)
    
    # 1. Establish the Acoustic Standing Wave (Topological Node)
    qc.h(range(qubits))
    
    # 2. Simulate Continuous Fluid Folding
    for step in range(steps):
        # The winding number dictates the geometric phase angle
        phase_angle = 2 * np.pi * ratio
        for i in range(qubits):
            qc.p(phase_angle, i)
            
        # Classical fluid turbulence hits the boundary
        for i in range(qubits):
            qc.rx(turbulence, i)
            
        # Entanglement refresh (maintaining the Torus ring boundary)
        for i in range(qubits - 1):
            qc.cx(i, i + 1)
        qc.cx(qubits - 1, 0)
        
    qc.measure_all()
    return qc

# Initialize the local M1 Aer Simulator
simulator = AerSimulator()

print("Simulating Micro-Vortex Stability across Toroidal winding cycles...")

# Execute the Golden Ratio (\phi)
qc_phi = build_fluid_folding_circuit(phi, num_qubits, iterations, turbulence_factor)
job_phi = simulator.run(transpile(qc_phi, simulator), shots=2048)
counts_phi = job_phi.result().get_counts()

# Execute the Rational Ratio
qc_rational = build_fluid_folding_circuit(rational_ratio, num_qubits, iterations, turbulence_factor)
job_rational = simulator.run(transpile(qc_rational, simulator), shots=2048)
counts_rational = job_rational.result().get_counts()

# Evaluate Structural Integrity
# An Inverse Participation Ratio (IPR) calculates how tightly the system groups its states.
# Complete kinetic collapse = flat distribution (~3.125%). Total protection = high concentration.
def calculate_structural_integrity(counts, shots):
    integrity = sum((count/shots)**2 for count in counts.values())
    return integrity * 100

phi_integrity = calculate_structural_integrity(counts_phi, 2048)
rational_integrity = calculate_structural_integrity(counts_rational, 2048)

print("--------------------------------------------------")
print(f"Topological Protection (\u03d5):  {phi_integrity:.2f}% Structural Integrity")
print(f"Resonance Disaster (0.5): {rational_integrity:.2f}% Structural Integrity")
print("--------------------------------------------------")
