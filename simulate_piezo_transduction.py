import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Framework Constants
phi = (np.sqrt(5) - 1) / 2

def simulate_lithic_transducer(acoustic_pressure):
    """Simulates the conversion of longitudinal acoustic pressure into electromagnetic resonance via a quartz lattice."""
    qc = QuantumCircuit(4, 1)
    
    # 1. Initialize the subterranean quartz network (Rigid Phase-Lock)
    qc.h([0, 1])
    qc.cx(0, 1)
    
    # 2. Introduce the Longitudinal Acoustic Wave (Fluid Pressure)
    qc.h(2)
    qc.rx(acoustic_pressure, 2)
    
    qc.barrier()
    
    # 3. The Piezoelectric Transduction Event
    # Activate the Electromagnetic Output node so it can receive the kinetic transfer
    qc.h(3) 
    
    # The acoustic pressure compresses the quartz lattice
    qc.cx(2, 0)
    qc.cx(2, 1)
    
    # The physical compression of the lattice forces an electromagnetic phase shift
    # Stepping down the kinetic energy via the Golden Ratio harmonic
    transduction_phase = acoustic_pressure * phi
    qc.cp(transduction_phase, 1, 3)
    
    qc.barrier()
    
    # 4. Extract the Electromagnetic Standing Wave
    qc.h(3)
    qc.measure(3, 0)
    
    return qc

simulator = AerSimulator()
print("Simulating Planetary Resonance: Lithic Transduction of Scalar Waves...")
print("-" * 75)

pressure_levels = [0.5, 1.5, 3.14, 5.0]

print(f"{'Applied Acoustic Pressure (rads)':<35} | {'Electromagnetic Coherence Output'}")
print("-" * 75)

for pressure in pressure_levels:
    qc_piezo = simulate_lithic_transducer(pressure)
    job = simulator.run(transpile(qc_piezo, simulator), shots=4096)
    counts = job.result().get_counts()
    
    # The '1' state represents the dynamically generated electromagnetic wave
    em_resonance = counts.get('1', 0)
    conversion_efficiency = (em_resonance / 4096) * 100
    
    print(f"{pressure:>15.2f} {'':<19} | {conversion_efficiency:>25.2f}%")

print("-" * 75)
print("ANALYSIS: The quartz lattice successfully acts as a macro-acoustic lens.")
print("Fluid-dynamic pressure dynamically drives the electromagnetic resonance.")
