---
phase: 8
wave: 1
gap_closure: false
---

# Phase 8 Execution Plan: Library Intelligence Registry

## Objective

Establish a "Library Intelligence" system that automatically detects dependencies (e.g., `react`, `fastapi`) and populates a dedicated knowledge graph with anti-patterns, idioms, and best practices.

## Tasks

<task>
**Title**: Create Directory Structure
**Description**: Create the `.agent/libraries` directory and its category subdirectories. Add a README explanation.
**Action**:
- Create `.agent/libraries/`
- Create `frontend/`, `backend/`, `security/`, `devops/`
- Write `README.md`
**Verify**:
- `test -d .agent/libraries/frontend`
</task>

<task>
**Title**: Build Dependency Scanner
**Description**: Create `scripts/scan_dependencies.py` to analyze `package.json` and `pyproject.toml`.
**Action**:
- Create `scripts/scan_dependencies.py`
- Implement JSON/TOML parsing
- Implement "Interest List" filtering (e.g., react, fastapi, next)
**Verify**:
- Run `python3 scripts/scan_dependencies.py` and check it output list of libs for this project (e.g. `fastapi` likely).
</task>

<task>
**Title**: Build Intelligence Fetcher
**Description**: Create `scripts/fetch_library_intel.py` to generate intelligence files.
**Action**:
- Create `scripts/fetch_library_intel.py`
- Trigger web search for "[lib] anti-patterns", "[lib] best practices"
- Format as `.agent/libraries/{category}/{lib}.md`
**Verify**:
- Run `python3 scripts/fetch_library_intel.py --lib fastapi`
- Check `.agent/libraries/backend/fastapi.md` exists and contains content.
</task>

<task>
**Title**: Create Sync Workflow
**Description**: Create the `/sync-libs` workflow.
**Action**:
- Create `.agent/workflows/sync-libs.md`
- Chain `scan_dependencies.py` output to `fetch_library_intel.py`
**Verify**:
- Run `/sync-libs` (simulated via manual step or run_command)
</task>
