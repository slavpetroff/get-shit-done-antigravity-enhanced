#!/usr/bin/env python3
import sys
import re

def main():
    """
    Extracts the 'type' attribute from a <task> block provided via stdin or file.
    Usage: cat task_block.xml | python3 scripts/gsd_extract_task_type.py
    """
    content = sys.stdin.read()
    
    # Regex to find <task ... type="...">
    # We look for 'type=' followed by quotes.
    match = re.search(r'<task[^>]*\btype=["\']([^"\']+)["\']', content)

    if match:
        print(match.group(1))
    else:
        # Default to 'auto' (Implementer) if no type specified
        print("auto")

if __name__ == "__main__":
    main()
