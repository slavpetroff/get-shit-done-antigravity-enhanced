---
phase: 13
wave: 1
gap_closure: false
---

# Phase 13 Execution Plan: Unified Context Recall

## Objective

Simplify context injection by creating a single `recall_context.py` script that aggregates Architecture (Memory), Skills, MCPs, and Library Intelligence, and integrate it into all workflows.

## Context

- **User Decision**: Use `ARCHITECTURE.md` as memory. "Recall" step should be unified.
- **Components**:
  - Memory: `.gsd/ARCHITECTURE.md`
  - Skills/MCPs: `scripts/gsd_select.py`
  - Libraries: `scripts/read_library_context.py`

## Tasks

<task type="auto">
<name>Create Unified Recall Script</name>
<files>scripts/recall_context.py</files>
<action>
Create `scripts/recall_context.py`:
- Import `read_library_context` and `gsd_select` logic (or call them via subprocess/import).
- Logic:
    1. Print "\n# 🧠 Project Context\n"
    2. Read & Print `.gsd/ARCHITECTURE.md` (if exists).
    3. Run `gsd_select` logic (with current args from sys.argv) and print output.
    4. Run `read_library_context` logic and print output.
- Ensure it handles missing files gracefully.
</action>
<verify>python3 scripts/recall_context.py "testing context"</verify>
<done>Script outputs Architecture, Skills, and Libs.</done>
</task>

<task type="auto">
<name>Update Workflows</name>
<files>.agent/workflows/map.md, .agent/workflows/plan.md, .agent/workflows/execute.md</files>
<action>
Refactor workflows to replace separate context steps with a single:
`python3 scripts/recall_context.py "{objective}"`

- In `/plan`: Replace `gsd_select` + `read_library_context` steps.
- In `/execute`: Replace `gsd_select` + `read_library_context` steps.
- In `/map`: Add if missing.
  </action>
  <verify>grep "recall_context.py" .agent/workflows/execute.md</verify>
  <done>Workflows updated.</done>
  </task>

<task type="auto">
<name>Sync Templates</name>
<files>.gsd/templates/scripts/, .gsd/templates/.agent/workflows/</files>
<action>
Update templates with the new script and updated workflows.
- `cp scripts/recall_context.py .gsd/templates/scripts/`
- `cp .agent/workflows/*.md .gsd/templates/.agent/workflows/`
</action>
<verify>test -f .gsd/templates/scripts/recall_context.py</verify>
<done>Templates synchronized.</done>
</task>
