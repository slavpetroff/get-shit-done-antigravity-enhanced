# ROADMAP.md

> **Current Phase**: Phase 1: Foundation
> **Milestone**: v1.1.0 — Intelligent Skills Discovery

## Must-Haves (from SPEC)

- [ ] Automated discovery script (`gsd_sync.py`)
- [ ] Selection logic script (`gsd_select.py`)
- [ ] `/sync-skills` workflow
- [ ] Integration with `/new-project`

## Phases

### Phase 2: Discovery Engine Implementation

**Status**: ✅ Complete
**Objective**: Implement `gsd_sync.py` to scan local and global paths.

### Phase 3: Selection Logic (The Reasoner)

**Status**: ✅ Complete
**Objective**: Implement `gsd_select.py` using keyword/context matching.

### Phase 4: Workflow Integration

**Status**: ✅ Complete
**Objective**: Add `/sync-skills` and update initialization workflows.

### Phase 5: Verification & Polish

**Status**: ✅ Complete
**Objective**: Comprehensive testing across platforms and documentation cleanup.

### Phase 6: Refine Implementation (Context RAG)

**Status**: ✅ Complete
**Objective**: Automate skill discovery and selection to ensure relevant skills are injected into prompts autonomously (RAG-style) without manual user commands.
**Depends on**: Phase 5
