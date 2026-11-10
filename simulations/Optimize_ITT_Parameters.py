#!/usr/bin/env python3
"""
Optimize_ITT_Parameters.py
Infinite Thread Theory - Parameter Optimization & Landscape Sweep

Performs a grid search across gamma_0 and eta to find the mathematical calibration
where the ITT Gated Damping model minimizes its statistical Total Variation 
Distance (D_TV) to the raw empirical data from ibm_marrakesh.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import json
import numpy as np

def run_optimization_sweep():
    profile_path = "results/simulation_telemetry/three_way_differential_profiles.json"
    hardware_path = "results/simulation_telemetry/empirical_hardware_fractional_profile.json"
    
    with open(profile_path, "r") as f:
        models = json.load(f)
    with open(hardware_path, "r") as f:
        hardware = json.load(f)

    all_basis_states = sorted(list(models["ideal_quantum"].keys()))
    prob_ideal = models["ideal_quantum"]
    
    # Generate search grids
    gamma_grid = np.linspace(0.01, 0.40, 40)
    eta_grid = np.linspace(0.0, 1.0, 50)
    
    best_d_tv = 999.0
    best_gamma = 0.0
    best_eta = 0.0

    # Read native classical alignment A_i based on original rotation vectors
    rotation_angles = [0.31, 0.57, 0.83, 1.09, 1.37, 1.61, 1.89, 2.17]
    A_i = np.array([abs(np.cos(a)) for a in rotation_angles])

    # Sweep the parameter grid
    for g0 in gamma_grid:
        for et in eta_grid:
            d_tv_temp = 0.0
            temp_itt = {}
            
            # Recompute the distribution for the current parameter point
            for state_str in all_basis_states:
                base_p = prob_ideal[state_str]
                bit_array = np.array([int(b) for b in state_str])
                
                survival_itt = 1.0
                for i in range(8):
                    if bit_array[i] == 1:
                        gamma_itt = g0 * (1.0 - et * A_i[i])
                        survival_itt *= (1.0 - gamma_itt)
                temp_itt[state_str] = base_p * survival_itt
            
            # Normalize trace
            s_itt = sum(temp_itt.values())
            for k in temp_itt.keys():
                temp_itt[k] /= s_itt
                
            # Compute distance to physical hardware
            for state_str in all_basis_states:
                p_hw = hardware.get(state_str, 0.0)
                d_tv_temp += abs(p_hw - temp_itt[state_str])
            d_tv_temp *= 0.5
            
            if d_tv_temp < best_d_tv:
                best_d_tv = d_tv_temp
                best_gamma = g0
                best_eta = et

    print("\n================ PARAMETER OPTIMIZATION SWEEP ================")
    print(f"Total Parameter Pairs Evaluated : {len(gamma_grid) * len(eta_grid)}")
    print(f"Minimum Achievable D_TV Target  : {best_d_tv:.4f}")
    print("--------------------------------------------------------------")
    print("Optimal Calibration Coordinates:")
    print(f"  Reference Hardware Damping (gamma_0) : {best_gamma:.3f}")
    print(f"  ITT Suppression Coefficient (eta)    : {best_eta:.3f}")
    print("==============================================================")
    print("[+] Optimization landscape completely mapped.")

if __name__ == "__main__":
    run_optimization_sweep()
