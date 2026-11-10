import sys
from qiskit_ibm_runtime import QiskitRuntimeService

def run_fetch():
    print("[*] Handshaking with IBM Quantum servers...")
    service = QiskitRuntimeService(channel="ibm_quantum_platform")
    job = service.job("dbp5eos4148s739tvgg0")
    print(f"[*] Server Registry Status: [{job.status()}]")
    
    print("[+] Extracting raw bit data packet...")
    res = job.result()
    pub = res[0]
    reg = list(pub.data.keys())[0]
    counts = pub.data[reg].get_counts()
    
    print("\n================== EMPIRICAL DATA RESULTS ==================")
    print(f"Total Successful Shots: {sum(counts.values())}")
    print("------------------------------------------------------------")
    for bitstring, hits in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"  State Vector |{bitstring}> : {hits} hits")
    print("============================================================")

if __name__ == "__main__":
    run_fetch()
