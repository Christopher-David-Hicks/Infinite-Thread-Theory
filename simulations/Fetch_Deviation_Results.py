#!/usr/bin/env python3
"""
Fetch_Deviation_Results.py
Infinite Thread Theory - Fractional Target Data Retrieval Suite

Pings the live IBM platform for the fractional rotation test payload,
downloads the raw 256-state empirical distribution matrix, and saves
the output ledger for three-way statistical distance evaluation.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import os
import json
import sys
from qiskit_ibm_runtime import QiskitRuntimeService

def pull_fractional_data(job_id):
    print(f"[*] Connecting to IBM Quantum Platform to retrieve Job ID: [{job_id}]...")
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
        job = service.job(job_id)
    except Exception as e:
        print(f"[-] Data retrieval handshake failed: {str(e)}")
        sys.exit(1)

    status = job.status()
    print(f"[*] Server Registry Status: [{status}]")

    if status != "DONE":
        print("[!] Notice: Your hardware job is still processing in the cloud queue.")
        return

    print("[+] Physical hardware execution complete! Unpacking 256-state data packet...")
    res = job.result()
    
    # Bulletproof V2 multi-layer extraction block
    try:
        # Step 1: Extract the first PUB result from the PrimitiveResult list
        pub_result = res[0]
        # Step 2: Grab the active classical register name dynamically
        reg_name = list(pub_result.data.keys())[0]
        counts = pub_result.data[reg_name].get_counts()
    except Exception as e:
        print(f"[*] Standard path detour: {str(e)}. Trying fallback layout container...")
        try:
            reg_name = list(res.data.keys())[0]
            counts = res.data[reg_name].get_counts()
        except Exception as e2:
            print(f"[-] Critical extraction block fault: {str(e2)}")
            print("[!] Alternative: You can view the raw percentages directly on your quantum.ibm.com dashboard.")
            return

    # Normalize counts to secure a strict probability distribution summing to 1.0
    total_shots = sum(counts.values())
    empirical_distribution = {
        state: float(hits / total_shots)
        for state, hits in sorted(counts.items(), key=lambda x: x[1], reverse=True)
    }

    # Export raw hardware results array to a dedicated json file ledger
    os.makedirs("results/simulation_telemetry", exist_ok=True)
    output_path = "results/simulation_telemetry/empirical_hardware_fractional_profile.json"
    with open(output_path, "w") as f:
        json.dump(empirical_distribution, f, indent=4)

    print("\n=================== EMPIRICAL DEVIATION DATA ===================")
    print(f"Total Successful Test Shots Processed: {total_shots}")
    print("Top 5 Measured Fractional State Realizations:")
    for state, prob in list(empirical_distribution.items())[:5]:
        print(f"  StateVector |{state}> : {prob * 100:.2f}% probability")
    print("----------------------------------------------------------------")
    print(f"[+] Empirical data ledger successfully exported to:\n    {output_path}")
    print("=================================================================")

if __name__ == "__main__":
    TARGET_JOB_ID = "dbp7dr5t7fqc7388suug"
    pull_fractional_data(TARGET_JOB_ID)
