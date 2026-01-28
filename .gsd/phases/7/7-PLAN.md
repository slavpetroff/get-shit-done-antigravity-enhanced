# PLAN: Phase 7 — Skills Registry Optimization

**Objective**: Refactor `SKILLS.md` to use a categorized index pointing to individual skill files, reducing file size and improving retrieval, while maintaining the machine-readable registry.

## 1. Tooling Implementation

### [NEW] `scripts/categorize_skills.py`

- **Input**: Scans `.agent/skills/**/*.md`
- **Logic**:
  - Extracts metadata (name, description, confidence).
  - Matches keywords to categories (e.g., "react" -> Frontend, "test" -> Quality).
  - Generates two sections:
    1. **Human Index**: Categorized headers with links to files.
    2. **Machine Registry**: XML block `<gsd_registry>` (JSON inside) for `gsd_select.py`.
- **Output**: Writes to `.gsd/SKILLS.md` (overwrites).

## 2. Workflow Integration

### [MODIFY] `.agent/workflows/sync-skills.md`

- **Add Step**: Run `python3 scripts/categorize_skills.py` after the initial sync/discovery step.
- **Goal**: Ensure every sync rebuilds the optimized index.

## 3. Validation & Integrity

### [MODIFY] `tests/test_context_integrity.py`

- **Update**: Ensure it validates the _new_ `SKILLS.md` format.
- **Assert**: `gsd_select.py` can still parse the registry and retrieve valid paths.

### [VERIFY] `scripts/gsd_verify_context.py`

- **Manual Test**: Run inspection to confirm injected skills are correctly formatted and paths are valid.

## Execution Steps

1. **Backup**: `cp .gsd/SKILLS.md .gsd/SKILLS_BACKUP.md`
2. **Develop**: Create `scripts/categorize_skills.py`.
3. **Execute**: Run the script to generate new `SKILLS.md`.
4. **Integrate**: Update `sync-skills.md`.
5. **Verify**: Run `test_context_integrity.py` and `gsd_select.py`.

## Verification Criteria

- [ ] `SKILLS.md` size reduced (target < 2000 lines, currently 14k).
- [ ] All skills present in both Index and Registry.
- [ ] `gsd_select.py` returns correct skill content (it might need to read the referenced file now if content isn't in registry? _Clarification: The user said "skills pointing to the location that could later specific skill when choosen could enhance prompts". This implies `gsd_select.py` might need to load the content from the file path if it's not in the registry._ -> **Decision**: Put the _full content_ in the registry JSON values so `gsd_select.py` doesn't need changing, OR update `gsd_select.py` to read files. **Let's keep full content in registry for now to minimize `gsd_select` breakage, or store path and update `gsd_select`. User said "fetching all relevant skills... like we do already". Storing path and reading on demand is cleaner for memory but requires code change. I will support path-based loading in `gsd_select.py` if needed, but start by keeping registry self-contained for compatibility if size allows, otherwise switch registry to paths.**)
      _Refinement_: If `SKILLS.md` is huge mainly due to the human-readable part, removing that alone helps. If the _registry_ is the bulk, we must switch `gsd_select.py` to lazy-load from paths. I will assume we want to switch to lazy-loading to solve the size issue properly.

**Revised Plan**:

- Update `gsd_select.py` to support `path` key in registry items and load content from file.
- Update `categorize_skills.py` to write `path` in registry instead of full `content`.
