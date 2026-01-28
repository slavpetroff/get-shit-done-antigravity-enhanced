#!/usr/bin/env python3
import sys
import json
import os

# scripts/propose_improvement.py
# Simulates the "Improver" agent who analyzes failures and proposes skill/workflow patches.

def main():
    if len(sys.argv) < 3:
        print("Usage: propose_improvement.py <task_objective> <failure_output>")
        sys.exit(1)

    task_objective = sys.argv[1]
    failure_output = sys.argv[2]
    
    # In a real agentic loop, we would ask an LLM here.
    # For now, we simulate the logic or returns a placeholder structure that the user can fill/LLM can invoke.
    
    # Heuristic: If failure mentions "command not found", check skills.
    # If failure mentions "file not found", check workflow steps.
    
    diagnosis = f"Task '{task_objective}' failed with output: {failure_output[:100]}..."
    
    # Placeholder proposal logic for V3.0 MVP
    # This script is intended to be called by the LLM (Assistant) or output a prompt for the LLM.
    # Since GSD uses the LLM to run scripts, this script primarily structures the *request* for improvement.
    
    proposal = {
        "diagnosis": diagnosis,
        "target_file": ".agent/skills/example_skill.md", # simplified
        "suggested_change": "Add missing dependency check step.",
        "rationale": "The task failed because a required tool was missing."
    }
    
    print(json.dumps(proposal, indent=2))

if __name__ == "__main__":
    main()
