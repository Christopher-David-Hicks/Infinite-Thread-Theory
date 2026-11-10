#!/usr/bin/env python3
"""
Quantum_Control_Group_Test.py
Infinite Thread Theory - Active Control Circuit Deployment Pipeline

Deploys an unentangled, high-noise control circuit to the IBM Quantum backend.
Provides the vital differential baseline to prove our multiplier gating math
selectively purifies the intentional ITT coherent signal rather than generic noise.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import sys
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

def run_quantum_control_test(api_token=None):
    if not api_token or api_token == "YOUR_IBM_API_TOKEN_HERE":
        print("[-] Error: Missing API token string.")
        sys.exit(1)

    print("[*] Connecting to IBM Quantum Platform (Control Group Mode)...")
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
    except Exception as e:
        print(f"[-] Authentication failed: {str(e)}")
        sys.exit(1)

    backend = service.least_busy(simulator=False, operational=True)
    print(f"[+] Control hardware target locked: [{backend.name}]")

    # --- Construct the Unentangled Control Circuit Space ---
    num_qubits = 8
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # CRITICAL CONTROL CHANGE: We do NOT apply Hadamard (H) or CNOT (CX) gates.
    # We leave the qubits completely decoupled, meaning any 1s recorded are pure noise.
    qc.barrier()
    qc.measure(range(num_qubits), range(num_qubits))

    print(f"[*] Transpiling unentangled register for [{backend.name}] layout...")
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pass_manager.run(qc)

    print(f"[*] Dispatching control payload to the [{backend.name}] queue...")
    sampler = SamplerV2(mode=backend)
    job = sampler.run([isa_circuit], shots=1024)
    
    print("\n================ CONTROL SUBMISSION SUCCESS ================")
    print(f"Control Job Identifier  : {job.job_id()}")
    print(f"Server Deployment State : QUEUED / RUNNING")
    print(f"Instruction Notice      : Save this Job ID for differential analysis.")
    print("=============================================================")
    
    return job.job_id()

if __name__ == "__main__":
    MY_TOKEN = "zValoN_s4tVYAkAb0L2NbCkh8R8ylxqCn4l6HwkMQDHF"
    run_quantum_control_test(api_token=MY_TOKEN)
