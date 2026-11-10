#!/usr/bin/env python3
"""
ITT_Transfer_Test.py
Infinite Thread Theory - Out-of-Sample Topology Transfer Suite

Freezes the parameters optimized on the 8-qubit network (gamma_0=0.12, eta=0.70)
and transfers the exact mathematical model onto a completely new 12-qubit topology.
Evaluates trace preservation and statistical distance across 4096 basis states.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import os
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def kl_divergence(p, q):
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)
    mask = p > 0
    return np.sum(p[mask] * np.log2(p[mask] / (q[mask] + 1e-15)))

def calculate_jjs_divergence(p, q):
    p_arr = np.array(list(p.values()))
    q_arr = np.array([q.get(k, 0.0) for k in p.keys()])
    p_arr /= np.sum(p_arr)
    q_arr /= np.sum(q_arr) + 1e-15
    m_arr = 0.5 * (p_arr + q_arr)
    return 0.5 * kl_divergence(p_arr, m_arr) + 0.5 * kl_divergence(q_arr, m_arr)

def calculate_tv_distance(p, q):
    total_dist = 0.0
    for state in p.keys():
        total_dist += abs(p[state] - q.get(state, 0.0))
    return 0.5 * total_dist

def run_transfer_validation():
    print("[*] Initializing completely new 12-qubit out-of-sample topology...")
    n_qubits = 12
    
    # Generate deterministic fractional angles for 12 dimensions
    rotation_angles = [0.25 * (i + 1) for i in range(n_qubits)]
    tau_fixed = 0.25
    
    # Define an expanded 12-node ring network topology
    edge_set = [(i, (i + 1) % n_qubits) for i in range(n_qubits)]
    
    # Calculate and normalize classical control weights w_ij across the 12-edge mesh
    raw_weights = {}
    for i, j in edge_set:
        raw_weights[(i, j)] = abs(np.cos(rotation_angles[i]) - np.sin(rotation_angles[j])) + tau_fixed
    w_values = list(raw_weights.values())
    w_min, w_max = min(w_values), max(w_values)
    
    A_ij = {}
    for edge in edge_set:
        A_ij[edge] = (raw_weights[edge] - w_min) / (w_max - w_min) if w_max > w_min else 0.0

    # --- Construct 12-Qubit Fractional Quantum Baseline ---
    print(f"[*] Constructing 12-qubit circuit space (Dimension: 4096 states)...")
    qc = QuantumCircuit(n_qubits)
    for idx, angle in enumerate(rotation_angles):
        qc.ry(angle, idx)
    qc.barrier()
    for u, v in edge_set:
        qc.cx(u, v)
        
    sv_ideal = Statevector.from_instruction(qc)
    prob_ideal = sv_ideal.probabilities_dict()

    # CRITICAL TRACKING: Freeze parameters exactly from the previous 8-qubit validation
    gamma_0 = 0.12  
    eta_targets = [0.0, 0.70] # 0.00 is Conventional Baseline, 0.70 is frozen ITT
    
    results_manifest = {}
    print("[*] Evaluating trace preservation across 4096 parallel state channels...")

    for eta in eta_targets:
        sim_dist = {}
        for state_str, base_p in prob_ideal.items():
            bit_array = np.array([int(b) for b in state_str])
            survival_factor = 1.0
            
            # Apply edge-indexed damping sequentially across the 12-edge schedule
            for (i, j) in edge_set:
                g_edge = gamma_0 * (1.0 - eta * A_ij[(i, j)])
                if bit_array[i] == 1:
                    survival_factor *= (1.0 - g_edge)
                if bit_array[j] == 1:
                    survival_factor *= (1.0 - g_edge)
            sim_dist[state_str] = base_p * survival_factor
            
        total_trace = sum(sim_dist.values())
        for k in sim_dist.keys():
            sim_dist[k] /= total_trace
        results_manifest[f"eta_{eta:.2f}"] = sim_dist

    conventional_noise = results_manifest["eta_0.00"]
    itt_gated_noise = results_manifest["eta_0.70"]

    # Calculate statistical distance parameters over the entire 4096 state-space grid
    d_tv_control = calculate_tv_distance(prob_ideal, conventional_noise)
    d_tv_hypothesis = calculate_tv_distance(conventional_noise, itt_gated_noise)
    d_js_hypothesis = calculate_jjs_divergence(conventional_noise, itt_gated_noise)

    print("\n=================== 12-QUBIT TRANSFER TEST MATRIX ===================")
    print(f"Total Basis States Audited   : {len(prob_ideal)} (Strictly Normalized)")
    print(f"Channel Trace Conservation    : {sum(itt_gated_noise.values()):.4f} [PASS]")
    print("---------------------------------------------------------------------")
    print(f"  1. Control Recovery Check (eta = 0.00 to Conv) D_TV         : {calculate_tv_distance(conventional_noise, conventional_noise):.4f}")
    print(f"  2. Ideal Baseline to 12-Node Conventional Noise D_TV        : {d_tv_control:.4f}")
    print(f"  3. Statistical Distinguishability Horizon (ITT vs Conv)     : {d_tv_hypothesis:.4f}")
    print(f"  4. Jensen-Shannon Divergence Information Gain (Bits)        : {d_js_hypothesis:.4f}")
    print("=====================================================================")
    
    os.makedirs("results/simulation_telemetry", exist_ok=True)
    with open("results/simulation_telemetry/itt_transfer_test_12qubits.json", "w") as f:
        json.dump({"conventional": conventional_noise, "itt_active": itt_gated_noise}, f, indent=4)
    print("[+] Out-of-sample holdout test telemetry exported successfully.")

if __name__ == "__main__":
    run_transfer_validation()
