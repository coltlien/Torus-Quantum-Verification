import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import GroverOperator, MCMT, ZGate

num_qubits = 6
total_states = 2**num_qubits

# The target "0 K Ground State Defect" embedded in the thermal noise.
# We represent this topologically protected state as the alternating integer '010101'
defect_state = '010101'

def create_thermal_phonon_noise(qubits, temperature_variance=0.15):
    """Generates the 2.7 K chaotic background acoustic noise."""
    qc = QuantumCircuit(qubits)
    qc.h(range(qubits))
    
    # Apply random phase kicks to simulate continuous kinetic thermal drag
    for i in range(qubits):
        random_phase = np.random.uniform(-temperature_variance, temperature_variance)
        qc.p(random_phase, i)
    return qc

def create_topological_oracle(qubits, target_state):
    """Marks the absolutely rigid, 0 K incompressible acoustic channel."""
    qc = QuantumCircuit(qubits)
    
    # Flip the states that match the zero-entropy defect
    for i, bit in enumerate(reversed(target_state)):
        if bit == '0':
            qc.x(i)
            
    # Multi-controlled Z gate to phase-flip the exact target defect
    qc.compose(MCMT(ZGate(), qubits - 1, 1), inplace=True)
    
    # Uncompute the flips
    for i, bit in enumerate(reversed(target_state)):
        if bit == '0':
            qc.x(i)
            
    return qc

print("Initializing the Universal Superfluid state...")
# 1. Build the baseline circuit with thermal phonon noise
fluid_circuit = create_thermal_phonon_noise(num_qubits)

# 2. Build the exact oracle marking the K -> infinity defect
oracle = create_topological_oracle(num_qubits, defect_state)

# 3. Construct the Asymptotic Filter (Amplitude Amplification)
# This simulates the phase-lock isolating the rigid channel from the thermal bath
grover_op = GroverOperator(oracle, state_preparation=fluid_circuit)

# Calculate optimal iterations for fluid folding
iterations = int(np.floor(np.pi / 4 * np.sqrt(total_states)))

qc_full = QuantumCircuit(num_qubits)
qc_full.compose(fluid_circuit, inplace=True)
for _ in range(iterations):
    qc_full.compose(grover_op, inplace=True)

qc_full.measure_all()

# Execute on the M1 optimized local simulator before deploying to IBM
simulator = AerSimulator()
transpiled_circuit = transpile(qc_full, simulator)

print(f"Executing Acoustic Asymptotic Filter across {total_states} micro-states...")
job = simulator.run(transpiled_circuit, shots=2048)
counts = job.result().get_counts()

# Locate the maximum isolated signal
max_state = max(counts, key=counts.get)
max_count = counts[max_state]
isolation_percentage = (max_count / 2048) * 100

print("--------------------------------------------------")
print("CMB Phonon Gas Extraction Results:")
print(f"Target 0 K Defect: {defect_state}")
print(f"Isolated Signal:   {max_state} at {isolation_percentage:.2f}% amplification")
print("--------------------------------------------------")
if max_state == defect_state and isolation_percentage > 90:
    print("SUCCESS: Localized infinite incompressibility mathematically isolated.")
    print("The rigid acoustic channel successfully bypassed the 2.7 K thermal drag.")
else:
    print("FAILURE: The zero-entropy defect was destroyed by thermal phonon scattering.")
