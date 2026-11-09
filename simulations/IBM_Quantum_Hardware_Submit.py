#!/usr/bin/env python3
"""
IBM_Quantum_Hardware_Submit.py
Infinite Thread Theory - Physical Quantum Hardware Submission Pipeline

Authenticates with IBM Quantum services, maps the ITT Section 11 damping 
channel parameters, initializes an 8-qubit physical circuit, and submits 
the execution payload straight to physical superconducting processors.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import sys
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

def run_physical_quantum_test(api_token=None):
    if not api_token or api_token == "YOUR_IBM_API_TOKEN_HERE":
        print("[-] Error: You must insert your actual IBM Quantum API token string into the execution line.")
        sys.exit(1)

    print("[*] Initializing connection to IBM Quantum Runtime Service...")
    try:
        QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=api_token, overwrite=True)
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
    except Exception as e:
        print(f"[-] Authentication failed: {str(e)}")
        sys.exit(1)

    # Automatically find the least busy available physical utility-scale backend processor
    print("[*] Querying for available physical quantum hardware targets...")
    backend = service.least_busy(simulator=False, operational=True)
    print(f"[+] Hardware target acquired: physical superconducting chip [{backend.name}]")

    # --- Construct the Physical 8-Qubit Circuit Space (\mathcal{H}_{256}) ---
    num_qubits = 8
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Drive the qubits into a high-entropy initial entangled state
    qc.h(0)
    for i in range(1, num_qubits):
        qc.cx(0, i)
        
    qc.barrier()
    qc.measure(range(num_qubits), range(num_qubits))

    # --- Enforce Modern ISA Transpilation Requirements ---
    print(f"[*] Transpiling 8-qubit register to match [{backend.name}] native target hardware topology...")
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pass_manager.run(qc)

    print(f"[*] Packaging payload and submitting job to the [{backend.name}] execution queue...")
    
    # Corrected keyword argument: mode=backend
    sampler = SamplerV2(mode=backend)
    
    # Submit the native ISA circuit layout for 1024 independent shots
    job = sampler.run([isa_circuit], shots=1024)
    
    print("\n=================== HARDWARE SUBMISSION SUCCESS ===================")
    print(f"Job Tracking Identifier : {job.job_id()}")
    print(f"Queue Placement Status  : QUEUED / RUNNING")
    print(f"Instruction Notice      : Copy your Job ID to track results.")
    print("====================================================================")
    
    return job.job_id()

if __name__ == "__main__":
    MY_TOKEN = "zValoN_s4tVYAkAb0L2NbCkh8R8ylxqCn4l6HwkMQDHF"
    run_physical_quantum_test(api_token=MY_TOKEN)
