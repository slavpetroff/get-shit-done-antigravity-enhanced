#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

LOG_FILE = ".gsd/logs/audit.jsonl"

def main():
    if not os.path.exists(LOG_FILE):
        print(f"No audit log found at {LOG_FILE}")
        return

    print(f"📊 Analyzing Context Logs: {LOG_FILE}\n")
    
    entries = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not entries:
        print("Log file is empty.")
        return

    # Summary Stats
    total_calls = len(entries)
    truncated_warns = 0
    empty_selections = 0
    
    print(f"Total Injections: {total_calls}")
    print("-" * 50)
    
    # Show last 5 entries
    for entry in entries[-5:]:
        ts = datetime.fromtimestamp(entry.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')
        context = entry.get('context', 'unknown')
        selection_count = len(entry.get('selected_ids', []))
        frag_len = entry.get('fragment_length', 0)
        
        status = "✅"
        if selection_count == 0:
            status = "⚠️  (No skills)"
            empty_selections += 1
        elif frag_len == 0:
            status = "❌ (Empty fragment)"
            truncated_warns += 1
            
        print(f"[{ts}] {status}")
        print(f"   Context: \"{context}\"")
        print(f"   Selected: {entry.get('selected_ids')}")
        print(f"   Payload: {frag_len} chars")
        print("")

    if empty_selections > 0 or truncated_warns > 0:
        print("-" * 50)
        print(f"WARNINGS: {empty_selections} empty selections, {truncated_warns} empty fragments")

if __name__ == "__main__":
    main()
