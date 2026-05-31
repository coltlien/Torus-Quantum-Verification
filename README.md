# Torus Macro-Acoustics: Quantum Verification Pipeline

**Author:** Colt Camron Lien  
**Affiliation:** University of Arkansas at Monticello  
**Framework:** The Fluid-Resonance Torus Framework

## Overview
This repository contains the hybrid classical-quantum execution pipeline designed to empirically verify the topological phase-locking mechanics proposed in the Fluid-Resonance Torus Framework. 

By bypassing standard cosmological vacuum models, this framework redefines the universe as a continuous, 3-dimensional Compressible Superfluid. This pipeline specifically tests the universal scaling equation:

$f_{micro} = f_{macro}\phi^m$

It achieves this by extracting raw, macroscopic fluid-dynamic pressure waves (measured as localized magnetic field vectors) from the Parker Solar Probe (PSP) and encoding them into a localized quantum topology (a parameterized CNOT ring) via IBM Quantum processors. 

## The Hybrid Pipeline
Due to the vast structural differences between classical data arrays and quantum state encoding, the verification is split into two discrete processes:

1. **Classical Extraction (`get_psp_data.py`)**: 
   Directly interfaces with NASA's Space Physics Data Facility (SPDF) to download Level 2 Radial-Tangential-Normal (RTN) data from the Parker Solar Probe. It dynamically bypasses broken visualization dependencies by extracting the raw multidimensional arrays directly from the `.cdf` files.
   
2. **Quantum State Encoding (`run_quantum_torus.py`)**:
   Normalizes the extracted macroscopic kinetic pressure data into quantum phase angles. These states are passed through a closed-loop CNOT topology representing the Toroidal boundary conditions. 

### Expected Output
If the macroscopic solar fluid is subject to chaotic turbulence, the IBM processor will output a scattered probability distribution across all possible qubit states. If the system is phase-locked and thermodynamically stable, constructive interference will force the quantum state to collapse into a highly specific, dominant alternating bitstring (e.g., `010101`), physically demonstrating macroscopic acoustic standing waves.

## Reproduction Instructions

### 1. Environment Setup
It is highly recommended to run this pipeline within an isolated Python 3.12+ virtual environment.

    python3 -m venv psp_env
    source psp_env/bin/activate
    pip install -r requirements.txt

### 2. Classical Data Extraction
Execute the extraction script to pull the raw arrays from NASA's servers.

    python get_psp_data.py

### 3. IBM Quantum Execution
To run the quantum verification, you must possess an active [IBM Quantum](https://quantum.ibm.com/) account and API token. Update the token authentication in the script if you have not saved your credentials locally, then execute:

    python run_quantum_torus.py
