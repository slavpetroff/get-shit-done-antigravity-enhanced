# Milestone: v1.2.0 — Context Observability & Validation

> **Goal**: Create measuring and validation tools to ensure GSD's automated context injection works correctly without truncation or formatting issues.

## Must-Haves

- [ ] Research report on prompt inspection methods
- [ ] `gsd_inspect.py` (or similar) to simulate workflow prompts
- [ ] Validation suite for skill injection integrity

## Phases

### Phase 1: Research Context Logging & Verification

**Status**: ⬜ Not Started
**Objective**: Investigate methods to capture or simulate the exact context (system prompt + user prompt + injected skills) sent to the LLM.

### Phase 2: Build Context Inspector Tools

**Status**: ⬜ Not Started
**Objective**: Create tooling to generate "dry run" prompts and analyze their token count and formatting.

### Phase 3: Validation Protocol & Stress Testing

**Status**: ⬜ Not Started
**Objective**: Assert that skills are not truncated and are correctly prioritized in various context sizes.

### Phase 4: Workflow Integration & Polish

**Status**: ⬜ Not Started
**Objective**: Integrate inspection tools into the workflow (e.g., `--dry-run`) and document findings.
