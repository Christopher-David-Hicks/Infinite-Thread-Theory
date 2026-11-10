#!/usr/bin/env python3
"""
Quantum_Deviation_Test.py
Infinite Thread Theory - Non-Standard Fractional Rotation Pipeline

Constructs an asymmetric, fractional rotation quantum circuit to produce
a complex multi-state map. Provides a non-standard differential baseline 
to explicitly test for deviations from textbook linear quantum mechanics.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

def run_quantum_deviation_test(api_token=None):
    if not api_token or api_token == "YOUR_IBM_API_TOKEN_HERE":
        print("[-] Error: Missing API token string.")
        sys.exit(1)

    print("[*] Connecting to IBM Quantum Platform (Deviation Test Mode)...")
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
    except Exception as e:
        print(f"[-] Authentication failed: {str(e)}")
        sys.exit(1)

    backend = service.least_busy(simulator=False, operational=True)
    print(f"[+] Active hardware target locked: [{backend.name}]")

    num_qubits = 8
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Apply progressive fractional rotations instead of standard 90-degree gates
    # This distributes state weights non-linearly across the register topology
    for i in range(num_qubits):
        fractional_angle = np.pi / (i + 2)
        qc.ry(fractional_angle, i)
        
    # Introduce an asymmetric, non-uniform entangling chain
    for i in range(num_qubits - 1):
        if i % 2 == 0:
            qc.cx(i, i + 1)
            
    qc.barrier()
    qc.measure(range(num_qubits), range(num_qubits))

    print(f"[*] Transpiling fractional register for [{backend.name}] native layout...")
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pass_manager.run(qc)

    print(f"[*] Dispatching non-standard payload to the [{backend.name}] queue...")
    sampler = SamplerV2(mode=backend)
    job = sampler.run([isa_circuit], shots=1024)
    
    print("\n================ DEVIATION SUBMISSION SUCCESS ================")
    print(f"Deviation Job Identifier : {job.job_id()}")
    print(f"Server Deployment State  : QUEUED / RUNNING")
    print(f"Instruction Notice       : Save this Job ID to pull non-linear counts.")
    print("===============================================================")
    
    return job.job_id()

if __name__ == "__main__":
    MY_TOKEN = "zValoN_s4tVYAkAb0L2NbCkh8R8ylxqCn4l6HwkMQDHF"
    run_quantum_deviation_test(api_token=MY_TOKEN)
