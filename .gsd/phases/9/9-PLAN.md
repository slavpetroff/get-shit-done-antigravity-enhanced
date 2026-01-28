---
phase: 9
wave: 1
gap_closure: false
---

# Phase 9 Execution Plan: Architecture Validator

## Objective

Build a "Smart" Architecture Validator that uses LLMs to check code against the patterns, idioms, and anti-patterns defined in the Library Intelligence Registry.

## Tasks

<task>
**Title**: Build Validator Script
**Description**: Create `scripts/validate_architecture.py`.
**Action**:
- Create script to:
    1. Identify active libraries (re-use `scan_dependencies.py` or simple check).
    2. Read content of matching `.agent/libraries/*/*.md`.
    3. Construct a prompt for the LLM: "Review [File/Diff] against these [Patterns]."
    4. Output a structured report (Pass/Fail/Warnings).
**Verify**:
- Run `python3 scripts/validate_architecture.py --files app/main.py` (mocking the LLM call if needed for initial test).
</task>

<task>
**Title**: Integrate with Verify Workflow
**Description**: Update `.agent/workflows/verify.md`.
**Action**:
- Add step: "Architecture Validation (LLM)"
- Run `python3 scripts/validate_architecture.py`
**Verify**:
- Check `/verify` workflow content.
</task>

<task>
**Title**: Integrate with New Milestone Workflow
**Description**: Update `.agent/workflows/new-milestone.md`.
**Action**:
- Add step to validate proposed architecture against registry.
**Verify**:
- Check `/new-milestone` workflow content.
</task>
