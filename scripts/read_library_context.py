import os
import sys
from scan_dependencies import identify_libraries

def get_library_context():
    """Reads content from active .agent/libraries/ files."""
    active_libs = identify_libraries()
    context = []
    
    if not active_libs:
        return "No active libraries identified from dependencies."

    context.append("# Library Intelligence Context")
    context.append("> Context loaded from `.agent/libraries` based on project dependencies.")
    context.append("")

    for lib in active_libs:
        category = lib['category']
        name = lib['name']
        path = os.path.join(".agent/libraries", category, f"{name}.md")
        
        if os.path.exists(path):
            try:
                context.append(f"## Library: {name} ({category})")
                with open(path, "r", encoding="utf-8") as f:
                    context.append(f.read())
                context.append("---")
            except Exception as e:
                print(f"Warn: Could not read {path}: {e}", file=sys.stderr)
        else:
            # Silent skip or warn if needed
            pass
                
    return "\n".join(context)

def main():
    print(get_library_context())

if __name__ == "__main__":
    main()
