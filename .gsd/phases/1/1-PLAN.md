---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Prototype Context Logging

## Objective

Validate the `fcntl` locking strategy for concurrent JSONL logging on macOS. We must prove that multiple processes writing large payloads related to skill injection do not corrupt the log file.

## Context

- .gsd/phases/1/RESEARCH.md
- **Requirement**: No data loss or corruption under high concurrency (waves of 5-10 agents).

## Tasks

<task type="auto">
  <name>Create Safe Logger Prototype</name>
  <files>prototypes/audit_logger.py</files>
  <action>
    Implement `safe_log_event(event_data, log_path)`:
    1. Open file in appending mode.
    2. Acquire exclusive lock (`fcntl.LOCK_EX`).
    3. Write JSON string + newline.
    4. Flush/Sync to disk.
    5. Release lock (`fcntl.LOCK_UN`).
    - Use a context manager pattern.
  </action>
  <verify>python3 prototypes/audit_logger.py</verify>
  <done>Script runs without error and creating a log entry.</done>
</task>

<task type="auto">
  <name>Create Stress Test</name>
  <files>prototypes/stress_test.py</files>
  <action>
    Implement a script that:
    1. Spawns 10 parallel processes using `multiprocessing`.
    2. Each process writes 100 large log entries (simulating skill dumps).
    3. Payload size should be >10KB to force non-atomic OS writes.
  </action>
  <verify>python3 prototypes/stress_test.py</verify>
  <done>Script completes and generates a large `.jsonl` file.</done>
</task>

<task type="auto">
  <name>Verify Log Integrity</name>
  <files>prototypes/verify_log.py</files>
  <action>
    Implement a script that:
    1. Reads the generate `.jsonl` lines.
    2. Parses each line as JSON.
    3. Asserts line count matches expected (10 processes * 100 entries = 1000 lines).
    4. Reports any JSONDecodeErrors (which would indicate corruption).
  </action>
  <verify>python3 prototypes/verify_log.py</verify>
  <done>Output confirms 1000 valid JSON lines.</done>
</task>

## Success Criteria

- [ ] `audit_logger.py` implements robust locking.
- [ ] Stress test generates heavy concurrent load.
- [ ] Verifier proves zero corruption (valid JSON) and zero data loss (correct count).
