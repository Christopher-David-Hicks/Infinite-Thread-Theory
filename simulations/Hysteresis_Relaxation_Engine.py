#!/usr/bin/env python3
import os
import csv
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class HysteresisRelaxationEngine:
    def __init__(self):
        self.U_GROUND = 0.1
        self.U_RECHARGE = 0.3
        self.U_TRIGGER = 0.8
        self.U_CEILING = 1.0
        self.LAMBDA_COEFF = 0.05
        self.CHARGE_GAIN = 0.08
        self.FLUX_EFFICIENCY = 0.95
        self.u_energy = self.U_GROUND
        self.purity_q = 1.0
        self.state_charging = True
        self.history_time = []
        self.history_energy = []
        self.history_purity = []
        self.history_state = []
        self.ledger_residuals = []
        self.cycle_count = 0
        self.boundary_violations = 0

    def calculate_multiplier_gate(self, current_u):
        clamped_u = max(0.0, min(current_u, self.U_CEILING))
        return (self.U_CEILING - clamped_u) * self.purity_q

    def execute_simulation_step(self, time_idx, environmental_noise):
        attenuation_gate = self.calculate_multiplier_gate(self.u_energy)
        if self.u_energy > self.U_CEILING or self.u_energy < 0.0:
            self.boundary_violations += 1
        if self.state_charging:
            delta_u = (self.CHARGE_GAIN * attenuation_gate) + (environmental_noise * 0.02)
            self.u_energy += delta_u
            self.purity_q = max(0.0, self.purity_q - (abs(environmental_noise) * 0.005))
            if self.u_energy >= self.U_TRIGGER:
                self.state_charging = False
                self.cycle_count += 1
        else:
            delta_u = - (self.LAMBDA_COEFF * self.u_energy)
            self.u_energy += delta_u
            self.purity_q = min(1.0, self.purity_q + 0.01)
            if self.u_energy <= self.U_RECHARGE:
                expected_energy_loss = self.U_TRIGGER - self.U_RECHARGE
                actual_flux_released = expected_energy_loss * self.FLUX_EFFICIENCY
                self.ledger_residuals.append(actual_flux_released)
                self.state_charging = True
        self.u_energy = max(0.0, min(self.u_energy, self.U_CEILING))
        self.history_time.append(time_idx)
        self.history_energy.append(self.u_energy)
        self.history_purity.append(self.purity_q)
        self.history_state.append(1.0 if self.state_charging else 0.0)

    def run_stress_test(self, simulation_window=500, seed_val=42):
        random.seed(seed_val)
        np.random.seed(seed_val)
        for t in range(simulation_window):
            baseline_noise = random.gauss(0.0, 1.0)
            self.execute_simulation_step(t, baseline_noise)
