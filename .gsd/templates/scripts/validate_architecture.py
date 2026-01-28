import os
import sys
import json
import argparse
from scan_dependencies import identify_libraries

def get_library_context():
    """Reads content from active .agent/libraries/ files."""
    active_libs = identify_libraries()
    context = []
    
    for lib in active_libs:
        category = lib['category']
        name = lib['name']
        path = os.path.join(".agent/libraries", category, f"{name}.md")
        
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    context.append(f"--- LIBRARY: {name} ---\n{f.read()}\n")
            except Exception as e:
                print(f"Warn: Could not read {path}: {e}", file=sys.stderr)
                
    return "\n".join(context)

def generate_validation_prompt(files, context):
    """Generates the prompt for the LLM."""
    
    prompt = f"""
# Architecture Validation Request

You are an Expert Software Architect. Validate the following code against the provided Library Intelligence.

## Library Intelligence (Context)
{context or "No specific library intelligence found."}

## Validation Rules
1. Check for Anti-Patterns listed in the intelligence.
2. Check for deviations from Best Practices.
3. Ignore issues unrelated to architecture (e.g. typos).
4. Be strict but fair.

## Code to Validate
"""
    for file_path in files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    prompt += f"\n--- FILE: {file_path} ---\n{f.read()}\n"
            except:
                pass
                
    prompt += "\n\n## Verdict (PASS/FAIL + Reasoning):"
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Generate Architecture Validation Prompt")
    parser.add_argument("--files", nargs="+", help="Files to validate", required=True)
    parser.add_argument("--check", action="store_true", help="Just output the prompt (dry run)")
    args = parser.parse_args()
    
    context = get_library_context()
    prompt = generate_validation_prompt(args.files, context)
    
    print(prompt)
    
    # In a real integration, we would send this to the LLM API here.
    # For GSD workflows, we output this to stdout so the Agent can read it and 'act' as the Validator.
    # or pipe it to an LLM tool if configured.

if __name__ == "__main__":
    main()
