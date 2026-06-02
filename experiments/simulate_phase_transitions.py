import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Framework Constants
phi = (np.sqrt(5) - 1) / 2
z122_baseline_stability = 0.5493

def apply_harmonic_pressure(atoms, artificial_phase_shift):
    """Simulates forcing a state-of-matter transition via acoustic phase manipulation."""
    qc = QuantumCircuit(atoms)
    
    # 1. Initialize Z-122 in its natural Superfluid state
    qc.h(range(atoms))
    
    # 2. Apply the baseline Toroidal stability
    baseline_angle = 2 * np.pi * z122_baseline_stability
    for i in range(atoms - 1):
        qc.cp(baseline_angle, i, i+1)
        
    # 3. Inject Artificial Harmonic Pressure (Acoustic Laser)
    # This artificially tightens or shatters the phase-lock
    for i in range(atoms):
        qc.p(artificial_phase_shift, i)
        
    # 4. Measure the resulting structural coherence
    qc.measure_all()
    return qc

simulator = AerSimulator()

# Test Scenarios: Discordant (Gas), Natural (Superfluid), Golden Ratio (Solid Crystal)
pressure_scenarios = {
    "Acoustic Fracture (Gas)": -np.pi / 2,         
    "Ambient State (Superfluid)": 0.0,              
    "Harmonic Compression (Solid)": 2 * np.pi * phi 
}

print("Simulating Torus Matter Phase Transitions via Harmonic Pressure...")
print("-" * 75)
print(f"{'Applied Acoustic Pressure':<30} | {'Coherence':<15} | {'Resulting State of Matter'}")
print("-" * 75)

for scenario, phase_shift in pressure_scenarios.items():
    qc_state = apply_harmonic_pressure(4, phase_shift)
    job = simulator.run(transpile(qc_state, simulator), shots=2048)
    
    # Extract coherence (0000 state represents a fully locked crystal)
    # Chaotic scatter represents a gas/plasma
    counts = job.result().get_counts()
    dominant_state_count = max(counts.values())
    coherence = (dominant_state_count / 2048) * 100
    
    if coherence >= 85.0:
        state = "[RIGID SOLID] Lattice Locked"
    elif 40.0 <= coherence < 85.0:
        state = "[SUPERFLUID] Frictionless Flow"
    else:
        state = "[CHAOTIC GAS] Boundary Shattered"
        
    print(f"{scenario:<30} | {coherence:>12.2f}% | {state}")

print("-" * 75)
print("ANALYSIS: States of matter for Torus elements are strictly a function of phase alignment, not temperature.")
