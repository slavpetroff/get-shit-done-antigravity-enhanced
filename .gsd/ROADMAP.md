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

# Milestone: v2.0 — Semantic Intelligence & Architecture

> **Goal**: Transform GSD from a workflow runner into an **Architectural Partner** by integrating library-specific knowledge graphs and enforcing patterns.

## Phase 8: Library Intelligence Registry

**Status**: ✅ Complete
**Objective**: Dedicated registry for Framework/Library knowledge, dynamically populated.
**Tasks**:

- [ ] Design Schema & Structure
- [ ] Build `scan_dependencies.py`
- [ ] Build `fetch_library_intel.py`
- [ ] Create `/sync-libs` workflow

**Tasks**:

- [ ] Create `scripts/categorize_skills.py`
- [ ] Update `sync-skills` workflow
- [ ] Refactor `gsd_select.py` for lazy loading (if needed)
- [ ] Verify `SKILLS.md` size reduction and link integrity

## Phase 9: Architecture Validator

**Status**: ✅ Complete
**Objective**: Build tooling to check code against defined patterns (e.g., "Architecture Enhancements").
**Tasks**:

- [ ] Define Validation Rules Schema
- [ ] Implement `gsd_validate.py`
- [ ] Integrate with `/verify` workflow

## Phase 10: Context-Aware Workflows

**Status**: ✅ Complete
**Objective**: Enhance `/plan` and `/execute` to dynamically pull form Library Intelligence based on project content.
**Tasks**:

- [ ] Update `gsd_select.py` to ingest Library Intelligence
- [ ] Update `/plan` workflow
- [ ] Update `/map` workflow

## Phase 11: Dogfooding & Template Synchronization

**Status**: ✅ Complete
**Objective**: Update project templates and self-apply strict architectural validation to the GSD codebase itself.
**Tasks**:

- [x] Update `.gsd/templates/` with new scripts/constants
- [x] Create `setup.sh` or update installation instructions
- [x] Run `/verify` on GSD repo (self-check)

# Milestone v3.0: Intelligent Agent Orchestration

**Goal**: Transform GSD from a passive context manager into an active, intelligent orchestrator that uses sub-agents and persistent memory.

## Phase 12: Sub-Agent Dispatch System

**Status**: 📅 Planned
**Objective**: Implement tools and workflows for delegating tasks to specialized sub-agents.
**Tasks**:

- [ ] Create `scripts/dispatch_agent.py` or `agent_tools.py`
- [ ] Define Sub-Agent Roles (Researcher, Implementer, Reviewer)
- [ ] Update `/execute` to optionally dispatch sub-agents

## Phase 13: Unified Context Recall (was Persistent Memory)

**Status**: ✅ Complete
**Objective**: Simplify context injection by creating a single `recall_context.py` script that aggregates Architecture (Memory), Skills, MCPs, and Library Intelligence.
**Tasks**:

- [x] Create `scripts/recall_context.py`
- [x] Update workflows to use Unified Recall
- [x] Sync Templates

## Phase 14: Kaizen Loop (Self-Optimization)

**Status**: ✅ Complete
**Objective**: Enable the system to propose and merge updates to its own skills.
**Tasks**:

- [x] Implement `scripts/propose_improvement.py`
- [x] Implement `scripts/review_proposal.py`
- [x] Integrate Kaizen Loop into `/execute` workflow
