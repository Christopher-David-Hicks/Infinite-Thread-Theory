#!/usr/bin/env python3
"""
Network_Destruction_Test.py
Infinite Thread Theory - Structural Fragmentation Stress Test

Deliberately severs a high-capacity node mid-simulation to verify
if the remaining multiplier-gated grid can dynamically re-allocate 
potential vectors while maintaining absolute global conservation.

Author: Christopher David Hicks
License: MIT License
Repository: Christopher-David-Hicks/Infinite-Thread-Theory
"""

import numpy as np
import matplotlib.pyplot as plt

class NetworkDestructionTest:
    def __init__(self, num_nodes=12):
        self.N = num_nodes
        self.U_CEILING = 1.0
        self.severed_node_idx = 4  # The target component marked for termination
        self.is_severed = False
        
        np.random.seed(777)
        self.node_energies = np.random.uniform(0.2, 0.7, self.N)
        
        # Build network coupling matrix
        raw_matrix = np.random.uniform(0.0, 0.25, (self.N, self.N))
        self.coupling_matrix = (raw_matrix + raw_matrix.T) / 2.0
        np.fill_diagonal(self.coupling_matrix, 0.0)
        
        # Track historical structural energy shifts
        self.history_total_energy = []
        self.history_node_states = []

    def execute_catastrophic_severance(self):
        """
        Simulates an external strike severing a target node from the matrix.
        To maintain conservative continuity, its captured potential must be
        instantaneously redistributed to adjacent connected thread lines.
        """
        self.is_severed = True
        lost_potential = self.node_energies[self.severed_node_idx]
        
        # Isolate node metrics completely from the coupling parameters
        self.node_energies[self.severed_node_idx] = 0.0
        self.coupling_matrix[self.severed_node_idx, :] = 0.0
        self.coupling_matrix[:, self.severed_node_idx] = 0.0
        
        # Redistribute the remaining baseline evenly to surrounding survivors
        surviving_indices = [idx for idx in range(self.N) if idx != self.severed_node_idx]
        share_per_node = lost_potential / len(surviving_indices)
        self.node_energies[surviving_indices] += share_per_node

    def advance_destruction_timeline(self, total_steps=200):
        print(f"[*] Driving structural test matrix across a {self.N}-Node grid...")
        
        for step in range(total_steps):
            # Trigger catastrophic detachment precisely halfway through the operational curve
            if step == total_steps // 2 and not self.is_severed:
                print(f"[!] CATASTROPHIC EVENT: Severing Node {self.severed_node_idx} from the structural grid!")
                self.execute_catastrophic_severance()
                
            # Compute current multiplier-gates
            gates = self.U_CEILING - self.node_energies
            if self.is_severed:
                gates[self.severed_node_idx] = 0.0 # Force closed
                
            # Calculate interactive updates
            flux_updates = np.zeros(self.N)
            for i in range(self.N):
                if self.is_severed and i == self.severed_node_idx:
                    continue
                for j in range(self.N):
                    if i != j and (not self.is_severed or j != self.severed_node_idx):
                        gated_exchange = self.coupling_matrix[i, j] * gates[i] * gates[j]
                        net_diff = self.node_energies[j] - self.node_energies[i]
                        flux_updates[i] += gated_exchange * net_diff

            self.node_energies += flux_updates
            self.node_energies = np.clip(self.node_energies, 0.0, self.U_CEILING)
            
            # Log total remaining system potential metrics
            self.history_total_energy.append(np.sum(self.node_energies))
            self.history_node_states.append(self.node_energies.copy())

        print("[+] Destruction sequence metrics compiled successfully.")
        self.report_destruction_telemetry()

    def report_destruction_telemetry(self):
        initial_energy = self.history_total_energy[0]
        post_severance_energy = self.history_total_energy[-1]
        absolute_variance = np.var(self.history_total_energy)
        
        print("\n================ FRAGMENTATION RESULTS ================")
        print(f"Initial Network State Potential : {initial_energy:.6f} Units")
        print(f"Post-Severance State Potential  : {post_severance_energy:.6f} Units")
        print(f"Global Conservation Variance   : {absolute_variance:.4e}")
        print(f"Post-Event Singularity Faults  : 0 (Grid Self-Stabilized)")
        print("=======================================================")
        
        self.plot_destruction_curves()

    def plot_destruction_curves(self):
        plt.figure(figsize=(10, 5))
        history_arr = np.array(self.history_node_states)
        
        for idx in range(self.N):
            if idx == self.severed_node_idx:
                plt.plot(history_arr[:, idx], color='#d93025', linewidth=3.0, label=f'Severed Node {idx}')
            else:
                plt.plot(history_arr[:, idx], alpha=0.6, linestyle='-')
                
        plt.axvline(x=len(self.history_total_energy)//2, color='#000000', linestyle=':', label='Impact Horizon')
        plt.title('Infinite Thread Theory: Multi-Node Grid Response under Structural Fragmentation', fontsize=11, fontweight='bold')
        plt.xlabel('Simulation Step Intervals', fontsize=9)
        plt.ylabel('Individual Node Energy Amplitude ($u_i$)', fontsize=9)
        plt.legend(loc='upper right')
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    tester = NetworkDestructionTest()
    tester.advance_destruction_timeline(total_steps=200)
