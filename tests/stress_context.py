import multiprocessing
import time
import subprocess
import os
from datetime import datetime

# Context length ~50KB
LARGE_CONTEXT = "test " * 10000 

def task(i):
    start = time.time()
    subprocess.run(
        ["python3", "scripts/gsd_select.py", LARGE_CONTEXT],
        capture_output=True
    )
    return time.time() - start

if __name__ == '__main__':
    CONCURRENCY = 100
    print(f"Starting stress test with {CONCURRENCY} concurrent processes...")
    
    start_time = time.time()
    
    with multiprocessing.Pool(CONCURRENCY) as p:
        latencies = p.map(task, range(CONCURRENCY))
        
    duration = time.time() - start_time
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    
    print(f"Total time: {duration:.2f}s")
    print(f"Average latency: {avg_latency:.2f}s")
    print(f"Max latency: {max_latency:.2f}s")
    
    if avg_latency > 1.0:
        print("WARN: Average latency > 1.0s")
    if max_latency > 5.0:
        print("FAIL: Max latency > 5.0s")
        exit(1)
        
    print("PASS: Stress test completed.")
