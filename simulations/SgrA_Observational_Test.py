#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
from SgrA_Data_Adapter import SgrADataAdapter

class SgrAObservationalTest:
    def __init__(self):
        self.M_SUN = 1.989e30
        self.G = 6.6743e-11
        self.C = 299792458
        self.M_SGR_A = 4.1e6 * self.M_SUN
        self.R_S_SGR_A = 2 * self.G * self.M_SGR_A / (self.C ** 2)

    def calculate_poisson_likelihood(self, observed_n, predicted_lambda):
        predicted_lambda = np.clip(predicted_lambda, 1e-10, None)
        log_n_factorial = np.zeros_like(observed_n, dtype=float)
        non_zero_idx = observed_n > 0
        log_n_factorial[non_zero_idx] = observed_n[non_zero_idx] * np.log(observed_n[non_zero_idx]) - observed_n[non_zero_idx]
        log_likelihood = observed_n * np.log(predicted_lambda) - predicted_lambda - log_n_factorial
        return np.sum(log_likelihood)

    def execute_validation_run(self):
        print("[*] Launching Astrophysical Verification Loop for Sgr A* Light Curves...")
        adapter = SgrADataAdapter()
        adapter.ingest_chandra_light_curve()
        
        time = adapter.observed_timestamps
        counts = adapter.observed_counts
        exposure = adapter.exposure_intervals
        
        split_idx = len(time) // 2
        test_counts = counts[split_idx:]
        test_exposure = exposure[split_idx:]
        
        predicted_lambda = adapter.generate_itt_forward_prediction()[split_idx:]
        log_L = self.calculate_poisson_likelihood(test_counts, predicted_lambda)
        
        print("\n================ DETECTOR ANALYSIS MATRIX ================")
        print(f"Sgr A* Target Core Scale (R_s) : {self.R_S_SGR_A:.4e} meters")
        print(f"Data Splitting Horizon         : 50% Train / 50% Verification")
        print(f"Poisson Log-Likelihood Score   : {log_L:.4f}")
        print(f"Statistical Exit Code Summary  : VALIDATION MATRIX COMPILED")
        print("==========================================================")

if __name__ == "__main__":
    tester = SgrAObservationalTest()
    tester.execute_validation_run()
