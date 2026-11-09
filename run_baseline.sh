#!/usr/bin/env bash
set -o pipefail
mkdir -p results/simulation_telemetry
LOG="results/simulation_telemetry/convergence_run_500s.log"
if [ -e "$LOG" ]; then
    echo "Baseline log already exists; refusing to overwrite."
    exit 1
fi
{
    echo "Infinite Thread Theory -- 500s Convergence Run"
    echo "Timestamp: $(date --iso-8601=seconds)"
    echo "Python version: $(python --version 2>&1)"
    echo "Operating system: $(uname -a)"
    echo "Git commit: $(git rev-parse HEAD 2>/dev/null || echo unavailable)"
    echo "----------------------------------------"
    python simulations/Timestep_Convergence_Check.py
    STATUS=$?
    echo "----------------------------------------"
    echo "Solver exit status: $STATUS"
    exit "$STATUS"
} 2>&1 | tee "$LOG"
STATUS=${PIPESTATUS}
echo "Captured solver status: $STATUS"
if [ "$STATUS" -ne 0 ]; then
    echo "Solver failed; checksum skipped."
    exit "$STATUS"
fi
echo "SHA-256:"
sha256sum "$LOG"
