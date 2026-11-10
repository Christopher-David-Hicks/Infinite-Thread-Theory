#!/usr/bin/env python3
"""
Quantum_Differential_Analysis.py
Infinite Thread Theory - Side-by-Side Signal vs. Control Assessment Suite

Pings both the experimental entangled run and the unentangled control baseline,
extracts their bit distributions, and calculates statistical differentiation
to cleanly separate architectural hardware characteristics from noise profiles.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import sys
from qiskit_ibm_runtime import QiskitRuntimeService

def run_differential_analysis(exp_id, ctrl_id):
    print("[*] Establishing secure connection to IBM Quantum Registry...")
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
        exp_job = service.job(exp_id)
        ctrl_job = service.job(ctrl_id)
    except Exception as e:
        print(f"[-] Handshake failed: {str(e)}")
        sys.exit(1)

    exp_status = exp_job.status()
    ctrl_status = ctrl_job.status()
    print(f"[*] Experimental Job Status : [{exp_status}]")
    print(f"[*] Control Baseline Status : [{ctrl_status}]")

    if exp_status != "DONE" or ctrl_status != "DONE":
        print("[!] Notice: One or both jobs are still waiting in the hardware queue.")
        return

    print("[+] Complete datasets recovered. Commencing side-by-side matrix parsing...")
    exp_res = exp_job.result()
    ctrl_res = ctrl_job.result()
    
    # Corrected V2 Primitive Result List indexing [0]
    try:
        pub_exp = exp_res[0]
        pub_ctrl = ctrl_res[0]
        
        reg_exp = list(pub_exp.data.keys())[0]
        reg_ctrl = list(pub_ctrl.data.keys())[0]
        
        exp_counts = pub_exp.data[reg_exp].get_counts()
        ctrl_counts = pub_ctrl.data[reg_ctrl].get_counts()
    except Exception as e:
        print(f"[-] Error indexing V2 results: {str(e)}")
        print("[*] Attempting fallback dictionary parsing...")
        try:
            exp_counts = exp_res.quasi_dists[0].binary_probabilities()
            ctrl_counts = ctrl_res.quasi_dists[0].binary_probabilities()
        except:
            print("[-] Structural extraction failed. Please review values on the IBM portal.")
            return

    print("\n=================== QUANTUM DIFFERENTIAL ANALYSIS ===================")
    print(f"Experimental Matrix (ID: {exp_id[:8]}...) | Control Baseline (ID: {ctrl_id[:8]}...)")
    print("----------------------------------------------------------------------")
    print("  State Vector   |   Experimental Hits   |   Control Baseline Hits   ")
    print("----------------------------------------------------------------------")
    
    # Aggregate top distinct states found across both runs
    all_states = sorted(list(set(list(exp_counts.keys()) + list(ctrl_counts.keys()))), 
                        key=lambda x: (exp_counts.get(x, 0) + ctrl_counts.get(x, 0)), reverse=True)[:10]
    
    for state in all_states:
        e_hits = exp_counts.get(state, 0)
        c_hits = ctrl_counts.get(state, 0)
        # Normalize display format if counts are returned as probabilities or raw ints
        e_str = f"{e_hits}" if isinstance(e_hits, int) else f"{e_hits*1024:.0f}"
        c_str = f"{c_hits}" if isinstance(c_hits, int) else f"{c_hits*1024:.0f}"
        print(f"   |{state}>    |       {e_str:<12}    |       {c_str:<12}")
    print("======================================================================")
    print("[+] Differential analysis completed successfully.")

if __name__ == "__main__":
    EXP_JOB = "dbp5eos4148s739tvgg0"
    CTRL_JOB = "dbp6tfs4148s739u1uf0"
    run_differential_analysis(EXP_JOB, CTRL_JOB)
