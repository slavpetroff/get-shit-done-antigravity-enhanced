import json
import sys

def verify_log(log_path, expected_count=1000):
    print(f"Verifying {log_path}...")
    
    lines = []
    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Log file not found!")
        sys.exit(1)
        
    print(f"Read {len(lines)} lines.")
    
    # Check count
    if len(lines) != expected_count:
        print(f"FAIL: Expected {expected_count} lines, found {len(lines)}")
        sys.exit(1)
        
    # Check JSON validity
    corrupt_count = 0
    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            # Optional: check payload length
            if len(data.get("payload", "")) != 10240:
                print(f"WARN: Line {i} has unexpected payload length")
        except json.JSONDecodeError as e:
            print(f"FAIL: Line {i} is corrupt: {e}")
            corrupt_count += 1
            
    if corrupt_count > 0:
        print(f"FAIL: Found {corrupt_count} corrupt lines")
        sys.exit(1)
        
    print("PASS: Log integrity verified.")

if __name__ == "__main__":
    verify_log(".gsd/logs/prototype_audit.jsonl")
