---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Build Validation & Stress Suite

## Objective

Create the automated testing infrastructure to rigorously validate context injection integrity, correct prioritization, and system stability under load.

## Context

- .gsd/DECISIONS.md (Hybrid validation, 100 concurrent users, deterministic ranking)
- scripts/gsd_select.py (Target for testing)
- scripts/gsd_verify_context.py (Manual tool reference)

## Tasks

<task type="auto">
  <name>Create Integrity Regression Test</name>
  <files>tests/test_context_integrity.py</files>
  <action>
    Create a `unittest` suite that:
    1. Sets up a temporary log location.
    2. Runs `gsd_select.py` (via subprocess) with a known "needle" in the context.
    3. Parses the generated log.
    4. Asserts that `full_fragment` contains the expected skill text (verifying no truncation).
    5. Asserts `fragment_length` matches the source skill length.
  </action>
  <verify>python3 -m unittest tests/test_context_integrity.py</verify>
  <done>Tests pass, confirming full injection integrity.</done>
</task>

<task type="auto">
  <name>Create Deterministic Ranking Test</name>
  <files>tests/test_ranking_simulation.py</files>
  <action>
    Create a `unittest` suite that:
    1. Defines test cases: {input: "python coding", expected: "python-patterns"}.
    2. Runs `gsd_select.py` for each case.
    3. Asserts that `selected_ids` in the log contains the expected ID.
    4. Validates the scoring logic logic works as intended.
  </action>
  <verify>python3 -m unittest tests/test_ranking_simulation.py</verify>
  <done>Tests pass, confirming "python" triggers "python-patterns".</done>
</task>

<task type="auto">
  <name>Build High-Load Stress Test</name>
  <files>tests/stress_context.py</files>
  <action>
    Create a massive concurrency script:
    1. Spawns 100 processes.
    2. Each process calls `gsd_select.py` with a 50KB simulated context.
    3. Verifies 100 log entries were created.
    4. Measures average execution time (overhead).
  </action>
  <verify>python3 tests/stress_context.py</verify>
  <done>Script reports success (100/100) and prints average latency.</done>
</task>

## Success Criteria

- [ ] All logical tests pass (integrity + ranking).
- [ ] Stress test sustains 100 concurrent users without file corruption.
- [ ] Latency overhead remains acceptable (<200ms).
