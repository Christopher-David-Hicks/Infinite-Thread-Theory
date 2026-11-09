import math

def execute_headless_integration(dt_value, total_steps_value):
    uc, ug, pin, ploss, v = 100.0, 10.0, 5.0, 1.0, 1.0
    beta, gamma, tau, utrig, urestart = 0.08, 0.12, 1.2, 98.0, 12.0
    u, Q, fsm_state, t = ug, 1.0, 1, 0.0
    first_trigger_time, first_reset_time = None, None
    min_Q, max_Q, cycles_completed, last_trigger_t = 1.0, 1.0, 0, None
    measured_periods, cycle_residuals = [], []
    current_cycle_work, current_cycle_u_start = 0.0, 0.0
    
    for _ in range(total_steps_value):
        if not (math.isfinite(u) and math.isfinite(Q) and math.isfinite(t)):
            raise FloatingPointError("Non-finite state encountered.")
        if not (0.5 - 1e-12 <= Q <= 1.0 + 1e-12):
            raise FloatingPointError(f"Purity interval breach: Q={Q}")
        u_old, t_old = u, t
        if fsm_state == 1:
            Lambda = Q * (1.0 - (u / uc))
            du_dt = Lambda * ((pin - ploss) / v)
            p_aligned = max(0.0, Lambda * pin)
            dQ_dt = beta * p_aligned * (1.0 - Q) - gamma * (Q - 0.5)
            u += du_dt * dt_value
            Q += dQ_dt * dt_value
            if Q > max_Q: max_Q = Q
            if Q < min_Q: min_Q = Q
            if u >= utrig:
                fsm_state = 0
                fraction = (utrig - u_old) / (u - u_old) if (u - u_old) != 0 else 0.0
                t_interp = t_old + fraction * dt_value
                if first_trigger_time is None: first_trigger_time = t_interp
                if last_trigger_t is not None: measured_periods.append(t_interp - last_trigger_t)
                last_trigger_t = t_interp
                current_cycle_u_start = u
                current_cycle_work = 0.0
        else:
            du_dt = -(u - ug) / tau
            dQ_dt = -gamma * (Q - 0.5)
            p_out = (v / tau) * (u - ug)
            current_cycle_work += p_out * dt_value
            u += du_dt * dt_value
            Q += dQ_dt * dt_value
            if Q > max_Q: max_Q = Q
            if Q < min_Q: min_Q = Q
            if u <= urestart:
                fsm_state = 1
                cycles_completed += 1
                fraction = (urestart - u_old) / (u - u_old) if (u - u_old) != 0 else 0.0
                t_interp = t_old + fraction * dt_value
                if first_reset_time is None: first_reset_time = t_interp
                e_expected = v * (current_cycle_u_start - u)
                cycle_residuals.append(abs(current_cycle_work - e_expected))
        t += dt_value

    avg_period = sum(measured_periods) / len(measured_periods) if measured_periods else None
    max_res = max(cycle_residuals) if cycle_residuals else 0.0
    mean_res = sum(cycle_residuals) / len(cycle_residuals) if cycle_residuals else 0.0
    return first_trigger_time, first_reset_time, min_Q, max_Q, max_res, mean_res, avg_period, cycles_completed, len(measured_periods)

def run_convergence_suite():
    print("==========================================================================================================")
    print("                 ITT COUPLED ENGINE -- TIMESTEP CONVERGENCE CONFORMANCE REPORT")
    print("==========================================================================================================")
    print(f"{'dt Step (s)':<10} | {'1st Trig (s)':<12} | {'1st ResetComp':<13} | {'Min Purity':<10} | {'Max Purity':<10} | {'Mean Res (J)':<11} | {'Period (s)':<10} | {'Cyc':<5} | {'Periods'}")
    print("----------------------------------------------------------------------------------------------------------")
    refinement_multipliers = (1, 2, 4, 8)
    base_dt, base_steps = 0.04, 12500
    prev_metrics = None
    convergence_data = []
    for multiplier in refinement_multipliers:
        current_dt = base_dt / multiplier
        current_steps = base_steps * multiplier
        trig, reset, qmin, qmax, max_res, mean_res, period, counts, periods_num = execute_headless_integration(current_dt, current_steps)
        trig_str = f"{trig:.4f}" if trig is not None else "N/A"
        reset_str = f"{reset:.4f}" if reset is not None else "N/A"
        period_str = f"{period:.4f}" if period is not None else "N/A"
        print(f"{current_dt:<10.4f} | {trig_str:<12} | {reset_str:<13} | {qmin:<10.4f} | {qmax:<10.4f} | {mean_res:<11.2e} | {period_str:<10} | {counts:<5} | {periods_num}")
        if prev_metrics is not None:
            eps_floor = 1e-7
            eps_trig = abs(trig - prev_metrics['trig']) / max(abs(trig), eps_floor) if (trig and prev_metrics['trig']) else float('nan')
            eps_reset = abs(reset - prev_metrics['reset']) / max(abs(reset), eps_floor) if (reset and prev_metrics['reset']) else float('nan')
            eps_qmin = abs(qmin - prev_metrics['qmin']) / max(abs(qmin), eps_floor)
            eps_qmax = abs(qmax - prev_metrics['qmax']) / max(abs(qmax), eps_floor)
            eps_period = abs(period - prev_metrics['period']) / max(abs(period), eps_floor) if (period and prev_metrics['period']) else float('nan')
            convergence_data.append({"dt": current_dt, "eps_trig": eps_trig, "eps_reset": eps_reset, "eps_qmin": eps_qmin, "eps_qmax": eps_qmax, "eps_period": eps_period})
        prev_metrics = {"trig": trig, "reset": reset, "qmin": qmin, "qmax": qmax, "period": period}
    print("----------------------------------------------------------------------------------------------------------")
    print("\n============================== SUCCESSIVE ERROR CONVERGENCE MATRIX ================================")
    print(f"{'Refinement dt (s)':<16} | {'Eps 1st Trig':<14} | {'Eps 1st Reset':<14} | {'Eps Min Purity':<14} | {'Eps Max Purity':<14} | {'Eps Cycle Period'}")
    print("----------------------------------------------------------------------------------------------------------")
    for d in convergence_data:
        t_e = f"{d['eps_trig']:.4e}" if not math.isnan(d['eps_trig']) else "N/A"
        r_e = f"{d['eps_reset']:.4e}" if not math.isnan(d['eps_reset']) else "N/A"
        print(f"{d['dt']:<16.4f} | {t_e:<14} | {r_e:<14} | {d['eps_qmin']:.4e} | {d['eps_qmax']:.4e} | {d['eps_period']:.4e}")
    print("==========================================================================================================")

if __name__ == '__main__':
    run_convergence_suite()
