---
phase: 11
wave: 1
gap_closure: false
---

# Phase 11 Execution Plan: Dogfooding & Template Synchronization

## Objective

Ensure that the "GSD v2.0" enhancements (Library Intelligence, Architecture Validator, Context-Aware Workflows) are propagated to the project templates, so new users get them immediately. Also, run the new validators on the GSD repo itself to prove concept ("dogfooding").

## Tasks

<task>
**Title**: Update Project Templates
**Description**: Ensure `.gsd/templates/` reflects the new reality.
**Action**:
- Check if `.gsd/templates/` needs to include the new scripts (`scripts/*.py`) or if they should be copied from `scripts/` during `/new-project`.
- **Target Items**:
    - `scripts/read_library_context.py` (Library Intelligence)
    - `scripts/validate_architecture.py` (Architecture Validator)
    - `scripts/categorize_skills.py` (Skills Registry)
    - `scripts/fetch_library_intel.py` (Library Intel)
    - `scripts/scan_dependencies.py` (Dependency Scanning)
    - `scripts/gsd_select.py` (Context Retrieval)
- Ensure MCP configuration guidance or setup scripts are included if applicable.
- Update `user-setup.md` or `README.md` in templates if they mention setup steps.
</task>

<task>
**Title**: Verify New Project Workflow
**Description**: Check `.agent/workflows/new-project.md` (if exists).
**Action**:
- Read `.agent/workflows/new-project.md`.
- Ensure it copies ALL the scripts listed above.
- Ensure it establishes the `.agent/skills` and `.agent/libraries` directory structures.
</task>

<task>
**Title**: Dogfooding - Run Architecture Validation
**Description**: Run the architecture validator on GSD itself.
**Action**:
- Run `python3 scripts/validate_architecture.py --check --files scripts/gsd_select.py` (or similar core file).
- Verify it produces sensible output.
</task>
