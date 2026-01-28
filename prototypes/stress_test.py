import multiprocessing
import time
import random
import os
from audit_logger import SafeAuditLogger

def worker_task(worker_id):
    logger = SafeAuditLogger(".gsd/logs/prototype_audit.jsonl")
    
    # Simulate a large skill payload (10KB)
    large_payload = "X" * 10240
    
    for i in range(100):
        event = {
            "worker_id": worker_id,
            "iter": i,
            "timestamp": time.time(),
            "payload": large_payload
        }
        logger.log_event(event)
        # Random sleep to interleave writes
        time.sleep(random.uniform(0.001, 0.005))

if __name__ == "__main__":
    # Clean up previous run
    if os.path.exists(".gsd/logs/prototype_audit.jsonl"):
        os.remove(".gsd/logs/prototype_audit.jsonl")
        
    processes = []
    print("Starting stress test with 10 processes...")
    
    for i in range(10):
        p = multiprocessing.Process(target=worker_task, args=(i,))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    print("Stress test complete.")
