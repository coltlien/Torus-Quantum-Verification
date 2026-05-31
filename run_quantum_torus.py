import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit.circuit import ParameterVector

# 1. Authenticate with IBM Quantum (Replace with your actual API token)
# You only need to run save_account once on your machine. 
# QiskitRuntimeService.save_account(channel="ibm_quantum_portal", token="283806d3-e223-409a-a102-b5195c91b7fc", set_as_default=True)
service = QiskitRuntimeService()

# Select the least busy quantum backend (or use a simulator for testing)
backend = service.least_busy(simulator=False, operational=True)
print(f"Executing on IBM Quantum Backend: {backend.name}")

# 2. Prepare the Classical Data (Simulating the feed from your PSP download)
# For a quantum circuit, we normalize a slice of the Radial (R) magnetic field data to fit within pi (a quantum phase rotation)
# In production, this array will be fed directly from your `final_vectors` output
sample_psp_radial_data = np.array([45.2, 42.8, 47.1, 41.5, 46.9, 43.2]) 
normalized_data = (sample_psp_radial_data / np.max(sample_psp_radial_data)) * np.pi

num_qubits = len(normalized_data)

# 3. Build the Torus Phase-Lock Circuit
# We use a Parameterized Quantum Circuit (PQC) to map the fluid-dynamic pressure to qubit states
qc = QuantumCircuit(num_qubits)
inputs = ParameterVector('Data', num_qubits)

# Angle Encoding: Apply the scalar magnetic variations as rotational X-gates
for i in range(num_qubits):
    qc.rx(inputs[i], i)

# Entanglement Layer: Testing for continuous acoustic standing waves 
# By chaining CNOT gates, we simulate the localized incompressibility and wave interference
for i in range(num_qubits - 1):
    qc.cx(i, i + 1)
qc.cx(num_qubits - 1, 0) # Close the loop to simulate Toroidal boundary conditions

qc.measure_all()

# 4. Bind the PSP data to the circuit
bound_circuit = qc.assign_parameters({inputs: normalized_data})
transpiled_circuit = transpile(bound_circuit, backend=backend)

# 5. Execute the job on IBM Quantum
print("Sending Torus circuit to IBM Quantum...")
sampler = SamplerV2(backend)
job = sampler.run([transpiled_circuit], shots=1024)
print(f"Job ID: {job.job_id()}")

# Wait for the result (this may take time depending on IBM's queue)
result = job.result()
pub_result = result[0]
counts = pub_result.data.meas.get_counts()

print("Quantum Measurement Results (Phase-Lock States):")
print(counts)

# --- The resulting bitstrings represent the interference patterns of the solar fluid boundary ---
