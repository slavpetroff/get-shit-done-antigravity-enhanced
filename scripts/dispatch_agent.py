#!/usr/bin/env python3
import os
import sys
import subprocess
import json

# dispatch_agent.py — The V3.0 Orchestrator
# This script bridges Persona, Skills, Architecture, and Library Intelligence
# to create an active System Instruction for the LLM.

def print_separator(char="━"):
    print(char * 60)

def load_persona(persona_name):
    """Loads the base persona file from .agent/personas/"""
    # Map task types to common persona names
    mapping = {
        "auto": "implementer",
        "verify": "reviewer",
        "research": "researcher"
    }
    persona_name = mapping.get(persona_name, persona_name)
    
    persona_path = f".agent/personas/{persona_name}.md"
    if not os.path.exists(persona_path):
        # Fallback to templates if local not yet hydrated
        persona_path = f".gsd/templates/.agent/personas/{persona_name}.md"
    
    if os.path.exists(persona_path):
        with open(persona_path, 'r') as f:
            return f.read()
    return f"# {persona_name.capitalize()} Persona\n(Warning: Persona file not found)"

def get_context(objective):
    """Calls recall_context.py to gather all intelligent fragments."""
    cmd = [sys.executable, "scripts/recall_context.py", objective]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error recalling context: {e}"

def main():
    if len(sys.argv) < 3:
        print("Usage: dispatch_agent.py <persona> <objective>")
        sys.exit(1)

    persona_name = sys.argv[1]
    objective = " ".join(sys.argv[2:])

    # 1. Load Persona
    persona_content = load_persona(persona_name)

    # 2. Gather Intelligent Context
    context_output = get_context(objective)

    # 3. Format the Active Directive
    directive = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 🚀 GSD SYSTEM DIRECTIVE: {persona_name.upper()} DISPATCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are now adopting the specialized persona below. 

### CRITICAL INSTRUCTION:
1. **SYSTEM PRIORITY**: The information in the 'GSD CONTEXT' section below contains your project's specific Memory (Architecture), Tools (Skills/MCPs), and Rules (Library Intelligence).
2. **OVERRIDE**: These sources MUST override your general training data if there is a conflict.
3. **TOOLING**: You are restricted to using the MCP tools and Skills explicitly listed in your hydrated intelligence.

---

{persona_content}

---

{context_output}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 END OF DISPATCH — PROCEED WITH OBJECTIVE: 
 {objective}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(directive)

if __name__ == "__main__":
    main()
