# Milestone: v1.2.0 — Context Observability & Validation

> **Goal**: Create measuring and validation tools to ensure GSD's automated context injection works correctly without truncation or formatting issues.

## Must-Haves

- [ ] Research report on prompt inspection methods
- [ ] `gsd_inspect.py` (or similar) to simulate workflow prompts
- [ ] Validation suite for skill injection integrity

## Phases

### Phase 1: Research Context Logging & Verification

**Status**: ✅ Complete
**Objective**: Investigate methods to capture or simulate the exact context (system prompt + user prompt + injected skills) sent to the LLM.

### Phase 2: Build Context Inspector Tools

**Status**: ✅ Complete
**Objective**: Create tooling to generate "dry run" prompts and analyze their token count and formatting.

### Phase 3: Validation Protocol & Stress Testing

**Status**: ✅ Complete
**Objective**: Assert that skills are not truncated and are correctly prioritized in various context sizes.

### Phase 4: Workflow Integration & Polish

**Status**: ✅ Complete
**Objective**: (Merged with Phase 3) Validation suite covers integration; polish applied via heuristic fixes.

### Phase 7: Skills Registry Optimization

**Status**: ✅ Complete
**Objective**: Refactor SKILLS.md to use a categorized index pointing to individual skill files to reduce file size and improve retrieval.
**Depends on**: Phase 6

**Tasks**:

- [ ] Create `scripts/categorize_skills.py`
- [ ] Update `sync-skills` workflow
- [ ] Refactor `gsd_select.py` for lazy loading (if needed)
- [ ] Verify `SKILLS.md` size reduction and link integrity
