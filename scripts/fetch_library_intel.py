import os
import json
import sys
import argparse
import subprocess

# Simple templates for when API is unavailable
TEMPLATE = """---
name: {name}
category: {category}
status: manual-review-required
---

# {name} Intelligence

> **Note**: This file was auto-generated and requires population.

## Anti-Patterns
- [ ] (Add anti-patterns here)

## Best Practices
- [ ] (Add usage idiomatics here)
"""

def get_existing_intel(category, name):
    path = os.path.join(".agent/libraries", category, f"{name}.md")
    return os.path.exists(path)

def generate_intel(lib, api_key=None):
    """
    Generates intelligence file. 
    In the future, this will call LLM APIs. 
    For MVP Phase 1, it creates a structured template.
    """
    category = lib['category']
    name = lib['name']
    
    path = os.path.join(".agent/libraries", category, f"{name}.md")
    
    # Check if exists
    if os.path.exists(path):
        print(f"  ✓ {name} (exists)")
        return

    print(f"  + Generating {name} ({category})...")
    
    # TODO: Integration with simple-llm-client or curl if keys present
    # content = fetch_from_llm(name) if api_key else TEMPLATE.format(...)
    
    content = TEMPLATE.format(name=name, category=category)
    
    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing {path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Fetch Library Intelligence")
    parser.add_argument("--scan", action="store_true", help="Run scanner first")
    args = parser.parse_args()
    
    libs = []
    
    if args.scan:
        # Run the scanner script and capture output
        try:
            result = subprocess.run(
                ["python3", "scripts/scan_dependencies.py"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            libs = json.loads(result.stdout)
        except Exception as e:
            print(f"Error running scanner: {e}")
            sys.exit(1)
    else:
        # Read from stdin if piped
        if not sys.stdin.isatty():
            try:
                libs = json.load(sys.stdin)
            except:
                pass
    
    if not libs:
        print("No libraries to process. Pipe JSON input or use --scan.")
        return

    print(f"Processing {len(libs)} libraries...")
    for lib in libs:
        generate_intel(lib)

if __name__ == "__main__":
    main()
