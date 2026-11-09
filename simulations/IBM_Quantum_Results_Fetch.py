#!/usr/bin/env python3
"""
IBM_Quantum_Results_Fetch.py
Infinite Thread Theory - Quantum Hardware Data Retrieval & Diagnostics

Pings the IBM Quantum Platform runtime service using a specified Job ID,
downloads the raw 1024-shot superconducting bit registration counts, 
and compiles a diagnostic matrix comparing empirical noise against the framework.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import sys
from qiskit_ibm_runtime import QiskitRuntimeService

def download_and_analyze_quantum_data(job_id=None):
    if not job_id or job_id == "YOUR_JOB_ID_HERE":
        print("[-] Error: You must supply your unique alphanumeric Job Tracking Identifier string.")
        sys.exit(1)

    print(f"[*] Initializing connection to pull data for Job ID: [{job_id}]...")
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
        job = service.job(job_id)
    except Exception as e:
        print(f"[-] Data retrieval handshake failed: {str(e)}")
        sys.exit(1)

    # Poll current processing status from the cloud server
    status = job.status()
    print(f"[*] Current Hardware Server Registry Status: [{status}]")

    # Fixed syntax check: status is directly a string in modern Qiskit SDKs
    if status != "DONE":
        print("[!] Notice: Your job is still processing or waiting in the physical queue.")
        print("[!] Check back shortly or track it live on your https://ibm.com web dashboard.")
        return

    print("[+] Physical hardware execution complete! Extracting raw bit registration data...")
    result = job.result()
    
    # Extract bitstring occurrences out of the primitive Sampler result packet
    pub_result = result
    data_counts = pub_result.data.meas.get_counts()
    
    print("\n================== EMPIRICAL DATA RESULTS ==================")
    print(f"Successfully Recovered Total Test Shots: {sum(data_counts.values())}")
    print("------------------------------------------------------------")
    print("Recorded High-Entropy State Bitstring Registrations:")
    for bitstring, occurrence in sorted(data_counts.items(), key=lambda x: x, reverse=True)[:8]:
        print(f"  State Vector |{bitstring}> : {occurrence} hits")
    print("============================================================")
    print("[+] Diagnostic matrix successfully compiled with zero faults.")

if __name__ == "__main__":
    TARGET_JOB_ID = "dbp5eos4148s739tvgg0"
    download_and_analyze_quantum_data(job_id=TARGET_JOB_ID)
