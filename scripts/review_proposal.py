#!/usr/bin/env python3
import sys
import json

# scripts/review_proposal.py
# Simulates the "Reviewer" sub-agent who validates proposed improvements.

def main():
    # Read proposal JSON from stdin
    try:
        input_data = sys.stdin.read()
        if not input_data:
             # Fallback for testing execution without pipe
             print("APPROVED: No input provided, assuming manual test.")
             return

        proposal = json.loads(input_data)
        
        # Validation Logic (Simulated)
        # 1. Is target_file a valid skill or workflow?
        # 2. Is the rationale sound?
        
        target = proposal.get("target_file", "")
        if ".agent/skills/" in target or ".agent/workflows/" in target:
             print(f"APPROVED: Change to {target} is within scope.")
        else:
             print(f"REJECTED: {target} is out of Kaizen scope.")
             
    except json.JSONDecodeError:
        print("REJECTED: Invalid JSON input.")
    except Exception as e:
        print(f"REJECTED: Error processing proposal: {e}")

if __name__ == "__main__":
    main()
