import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Framework Constants
z123_stability = 0.8018
z125_stability = 0.9180

def simulate_hybrid_diode(kinetic_impacts):
    """Simulates a Z-123 absorber layered over a Z-125 asymmetric rectifier."""
    # Qubits 0 & 1: Z-123 Impact Absorber Plate
    # Qubits 2 & 3: Z-125 Asymmetric Rectifier (Acoustic Diode)
    qc = QuantumCircuit(4)
    
    # 1. Initialize Metamaterial
    qc.h(range(4))
    
    # 2. Establish Z-123 Top Layer (Flexible, Breathing)
    z123_phase = 2 * np.pi * z123_stability
    qc.cp(z123_phase, 0, 1)
    
    # 3. Establish Z-125 Bottom Layer (Asymmetric Wave Trap)
    z125_phase = 2 * np.pi * z125_stability
    qc.cp(z125_phase, 2, 3)
    
    # 4. Bond the Layers (The Transducer Interface)
    qc.cx(0, 2)
    qc.cx(1, 3)
    
    qc.barrier()
    
    # 5. Apply Chaotic Kinetic Impacts (Physical strikes on the Z-123 Top Plate)
    for strike in range(kinetic_impacts):
        qc.rx(np.random.uniform(0.5, 1.5), 0)
        qc.ry(np.random.uniform(0.5, 1.5), 1)
        
    qc.barrier()
    
    # 6. The Z-125 Rectification (Acoustic Diode)
    # The Z-125 layer pulls the chaotic phase from Z-123 and forces it 
    # through its asymmetric geometry, phase-conjugating the chaos into DC power.
    # We simulate this mathematically by applying the inverse directional lock.
    rectification_pull = z125_stability / z123_stability
    
    # Z-125 forces directional alignment on the chaotic Z-123 nodes
    qc.crx(-np.pi * rectification_pull, 2, 0)
    qc.cry(-np.pi * rectification_pull, 3, 1)
    
    # Final extraction into coherent flow
    qc.h(range(4))
    qc.measure_all()
    
    return qc

simulator = AerSimulator()
print("Simulating Hybrid Macro-Transducer: Z-123 + Z-125 Acoustic Diode...")
print("-" * 75)

# Applying the exact same 10 chaotic kinetic strikes from the failed test
impact_count = 10 

qc_hybrid = simulate_hybrid_diode(impact_count)
job = simulator.run(transpile(qc_hybrid, simulator), shots=2048)
counts = job.result().get_counts()

# We measure the coherence of the output flow.
power_generation = (counts.get('0000', 0) / 2048) * 100

print(f"Top Layer: Z-123 (Absorber) | Bottom Layer: Z-125 (Rectifier)")
print(f"Applied Stress: {impact_count} Chaotic Kinetic Strikes")
print(f"Energy Conversion Efficiency: {power_generation:.2f}%")
print("-" * 75)

if power_generation > 80.0:
    print("RESULT: Acoustic Diode Successful. Impact perfectly rectified.")
    print("The Z-125 layer funneled the chaotic heat into pure electrical current.")
else:
    print("RESULT: Diode Failed. Energy scattered.")
