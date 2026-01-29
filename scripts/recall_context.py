#!/usr/bin/env python3
import os
import sys
import subprocess
import json

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
        with open(arch_file, 'r') as f:
            return f.read()
    return ""

def recall_skills(args):
    script = "scripts/gsd_select.py"
    if os.path.exists(script):
        cmd = [sys.executable, script] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error executing skill selection: {e}"
    return "Skill selection script not found."

def recall_libraries():
    script = "scripts/read_library_context.py"
    if os.path.exists(script):
        try:
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error reading library context: {e}"
    return "Library intelligence script not found."

def main():
    use_json = "--json" in sys.argv
    clean_args = [a for a in sys.argv[1:] if a != "--json"]

    arch = recall_architecture()
    skills_output = recall_skills(clean_args)
    libs = recall_libraries()

    if use_json:
        # Attempt to parse skills_output as it's usually JSON from gsd_select.py
        try:
            skills_data = json.loads(skills_output)
        except:
            skills_data = {"raw": skills_output}

        data = {
            "architecture": arch,
            "skills_mcps": skills_data,
            "library_intelligence": libs
        }
        print(json.dumps(data, indent=2))
    else:
        print_banner("ARCHITECTURE (MEMORY)")
        print(arch if arch else "No architecture memory found.")
        
        print_banner("RELEVANT SKILLS & MCPS")
        print(skills_output)
        
        print_banner("LIBRARY INTELLIGENCE")
        print(libs)

if __name__ == "__main__":
    main()
