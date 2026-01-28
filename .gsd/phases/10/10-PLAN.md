---
phase: 10
wave: 1
gap_closure: false
---

# Phase 10 Execution Plan: Context-Aware Workflows

## Objective

Enhance `/plan`, `/execute`, and `/map` workflows to explicitly pull relevant Library Intelligence (patterns, anti-patterns) into the context.

## Tasks

<task>
**Title**: Build Context Reader Script
**Description**: Create `scripts/read_library_context.py`.
**Action**:
- Create script to:
    1. Scan dependencies (using `scan_dependencies.py`).
    2. Read matching files from `.agent/libraries/`.
    3. Output formatted text (Markdown) to stdout.
**Verify**:
- Run `python3 scripts/read_library_context.py` and check output.
</task>

<task>
**Title**: Update /map Workflow
**Description**: Inject intelligence into the Architect's context.
**Action**:
- Modify `.agent/workflows/map.md`.
- Add step: "Read Library Intelligence".
- Command: `python3 scripts/read_library_context.py`.
**Verify**:
- View workflow file.
</task>

<task>
**Title**: Update /plan Workflow
**Description**: Inject intelligence into the Strategist's context.
**Action**:
- Modify `.agent/workflows/plan.md`.
- Add context step: "Read Strategy & Intelligence".
**Verify**:
- View workflow file.
</task>

<task>
**Title**: Update /execute Workflow
**Description**: Inject intelligence into the Engineer's context.
**Action**:
- Modify `.agent/workflows/execute.md`.
- Add step in the Plan Loading or Execution loop to reference library patterns.
**Verify**:
- View workflow file.
</task>
