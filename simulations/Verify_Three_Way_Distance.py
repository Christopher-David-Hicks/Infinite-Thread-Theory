#!/usr/bin/env python3
"""
Verify_Three_Way_Distance.py
Infinite Thread Theory - Three-Way Statistical Distance Validator

Loads the full 256-state empirical hardware dataset and calculates the exact
Total Variation Distance (D_TV) against the Ideal, Conventional, and ITT models
to determine which framework mathematically matches real physical execution.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import json
import numpy as np

def calculate_statistical_distances():
    profile_path = "results/simulation_telemetry/three_way_differential_profiles.json"
    hardware_path = "results/simulation_telemetry/empirical_hardware_fractional_profile.json"
    
    try:
        with open(profile_path, "r") as f:
            models = json.load(f)
        with open(hardware_path, "r") as f:
            hardware = json.load(f)
    except Exception as e:
        print(f"[-] Error loading data files: {str(e)}")
        return

    # Align all 256 state bins across datasets
    all_basis_states = sorted(list(models["ideal_quantum"].keys()))
    
    d_tv_ideal = 0.0
    d_tv_conv = 0.0
    d_tv_itt = 0.0

    # Calculate Total Variation Distance: D_TV = 0.5 * sum(|P(x) - Q(x)|)
    for state in all_basis_states:
        p_hw = hardware.get(state, 0.0)
        
        p_id = models["ideal_quantum"].get(state, 0.0)
        p_cn = models["conventional_noise"].get(state, 0.0)
        p_itt = models["itt_modified"].get(state, 0.0)
        
        d_tv_ideal += abs(p_hw - p_id)
        d_tv_conv += abs(p_hw - p_cn)
        d_tv_itt += abs(p_hw - p_itt)

    d_tv_ideal *= 0.5
    d_tv_conv *= 0.5
    d_tv_itt *= 0.5

    print("\n=================== STATISTICAL DISTANCE VERIFICATION ===================")
    print(f"Total Basis States Audited  : {len(all_basis_states)}")
    print("Calculated Total Variation Distance (D_TV) to Physical Hardware:")
    print("-------------------------------------------------------------------------")
    print(f"  1. Ideal Textbook Quantum Baseline D_TV : {d_tv_ideal:.4f}")
    print(f"  2. Conventional Hardware Noise Model D_TV: {d_tv_conv:.4f}")
    print(f"  3. ITT Gated Damping Channel Model D_TV  : {d_tv_itt:.4f}")
    print("=========================================================================")
    
    min_dist = min(d_tv_ideal, d_tv_conv, d_tv_itt)
    if min_dist == d_tv_itt:
        print("[+] CONCLUSION: The physical hardware correlates closest with the ITT framework.")
    elif min_dist == d_tv_conv:
        print("[+] CONCLUSION: The physical hardware correlates closest with Conventional Noise.")
    else:
        print("[+] CONCLUSION: The physical hardware correlates closest with Ideal Quantum mechanics.")

if __name__ == "__main__":
    calculate_statistical_distances()
