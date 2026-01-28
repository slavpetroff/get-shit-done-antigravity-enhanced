---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Implement Integrated Context Logging

## Objective

Integrate the safe logging logic (prototyped in Phase 1) directly into `gsd_select.py` and build the temporary verification tool.

## Context

- .gsd/DECISIONS.md (Integrated Logic, No Proxy)
- prototypes/audit_logger.py (Reference implementation)
- scripts/gsd_select.py (Target file)

## Tasks

<task type="auto">
  <name>Integrate Logging into gsd_select.py</name>
  <files>scripts/gsd_select.py</files>
  <action>
    Modify `scripts/gsd_select.py` to:
    1. Import `fcntl`, `json`, `time`, `os`.
    2. Add `log_context_selection(context, selected_items, prompt_fragment)` function.
    3. Call this function before the script exits/prints.
    4. Log to `.gsd/logs/audit.jsonl`.
    - Use key fields: timestamp, pid, context, selected_ids, fragment_length, full_fragment.
  </action>
  <verify>python3 scripts/gsd_select.py "test logging integration" && cat .gsd/logs/audit.jsonl | grep "test logging integration"</verify>
  <done>Script runs normally AND appends a valid JSON line to the log.</done>
</task>

<task type="auto">
  <name>Create Context Verifier Tool</name>
  <files>scripts/gsd_verify_context.py</files>
  <action>
    Create a standalone script that:
    1. Reads `.gsd/logs/audit.jsonl`.
    2. For each entry, calculates success metrics (was anything selected?).
    3. [Crucial] Checks if `full_fragment` matches expectations (not empty).
    4. Prints a report of recent context injections.
  </action>
  <verify>python3 scripts/gsd_verify_context.py</verify>
  <done>Script displays a summary of the log file.</done>
</task>

## Success Criteria

- [ ] `gsd_select.py` transparently logs every execution.
- [ ] `gsd_verify_context.py` can read and summarize those logs.
- [ ] No performance regression in `gsd_select.py` (still <1s).
