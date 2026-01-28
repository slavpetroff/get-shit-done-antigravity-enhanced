#!/usr/bin/env python3
import os
import sys
import subprocess

# Unified Context Recall Script
# Aggregates:
# 1. Architecture (Memory) - .gsd/ARCHITECTURE.md
# 2. Skills/MCPs - scripts/gsd_select.py
# 3. Library Intelligence - scripts/read_library_context.py

def print_banner(title):
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f" 🧠 GSD CONTEXT: {title}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def recall_architecture():
    arch_file = ".gsd/ARCHITECTURE.md"
    if os.path.exists(arch_file):
        print_banner("ARCHITECTURE (MEMORY)")
        try:
            with open(arch_file, 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading architecture: {e}")
    else:
        # Graceful fallback - maybe project is new
        pass

def recall_skills(args):
    print_banner("RELEVANT SKILLS & MCPS")
    script = "scripts/gsd_select.py"
    if os.path.exists(script):
        # Pass through all arguments to gsd_select
        cmd = [sys.executable, script] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Skill Selection Warnings:\n{result.stderr}", file=sys.stderr)
        except Exception as e:
            print(f"Error executing skill selection: {e}")
    else:
        print("Skill selection script not found.")

def recall_libraries():
    print_banner("LIBRARY INTELLIGENCE")
    script = "scripts/read_library_context.py"
    if os.path.exists(script):
        try:
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                 pass # Library script often outputs innocent warnings to stderr
        except Exception as e:
            print(f"Error reading library context: {e}")
    else:
        print("Library intelligence script not found.")

def main():
    # 1. Recall Architecture (Memory)
    recall_architecture()
    
    # 2. Recall Skills (Contextual)
    # Pass command line args (objectives) to skill selector
    recall_skills(sys.argv[1:])
    
    # 3. Recall Library Intelligence (Contextual)
    recall_libraries()

if __name__ == "__main__":
    main()
