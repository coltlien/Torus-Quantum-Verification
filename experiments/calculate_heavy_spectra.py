import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Framework Constants
phi = (np.sqrt(5) - 1) / 2
# Fundamental Torus macro-acoustic baseline (approx 433 THz, standard H-alpha proxy)
f_macro_hz = 4.33e14  
# The 8th Concentric Ring (Period 8 of the acoustic table)
octave_shell = 8      

# JWST Target Ranges
# NIRCam and MIRI instruments detect from ~0.6 to 28.5 micrometers
jwst_min_um = 0.6
jwst_max_um = 28.5
speed_of_light = 299792458

def calculate_phase_locked_emission(atomic_number):
    """Calculates the theoretical emission spectra using Torus fluid dynamics."""
    # 1. Translate Atomic Number into a Toroidal Phase Angle
    # Utilizing the radial geometry: shifting across the 8-sector boundary
    radial_position = atomic_number % 8
    if radial_position == 0: 
        radial_position = 8
        
    phase_angle = 2 * np.pi * (radial_position * phi)
    
    # 2. Quantum Interference Circuit
    # Simulates the acoustic boundary folding of the specific heavy element
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.p(phase_angle, 0)
    qc.h(0)
    qc.measure_all()
    
    # 3. Execute Local Simulator
    simulator = AerSimulator()
    job = simulator.run(transpile(qc, simulator), shots=2048)
    counts = job.result().get_counts()
    
    # 4. Extract Constructive Interference Probability (Structural Stability)
    stability = counts.get('0', 0) / 2048
    
    # 5. Apply the Universal Scaling Equation: f_micro = f_macro * phi^m * stability
    f_micro = f_macro_hz * (phi ** octave_shell) * stability
    
    # 6. Convert Frequency (Hz) to Wavelength (micrometers) for JWST scanning
    if f_micro > 0:
        wavelength_m = speed_of_light / f_micro
        wavelength_um = wavelength_m * 1e6
    else:
        wavelength_um = float('inf')
        
    return stability, wavelength_um

print("Generating JWST Emission Signatures for Island of Stability (Octave 8)...")
print("-" * 75)
print(f"{'Element (Z)':<15} | {'Phase Stability':<20} | {'JWST Target Wavelength':<30}")
print("-" * 75)

for Z in range(119, 127):
    stability, wavelength = calculate_phase_locked_emission(Z)
    
    # Filter for JWST observability limits
    if jwst_min_um <= wavelength <= jwst_max_um:
        visibility = "[PRIME JWST TARGET]"
    else:
        visibility = "[OUT OF RANGE]"
        
    print(f"Element {Z:<7} | {stability*100:>6.2f}% Phase-Lock  | {wavelength:>8.2f} µm  {visibility}")
print("-" * 75)
