---
phase: 1
level: 2
researched_at: 2026-01-28
---

# Phase 1 Research: Context Logging & Verification

## Questions Investigated

1. **Concurrency Strategy**: How to safely log huge JSON payloads (100KB+) from multiple processes to a single file?
2. **Schema Definition**: What JSON structure answers "was this prompt truncated?"
3. **Verification Logic**: How to programmatically assert correctness?

## Findings

### Concurrency & Atomicity

Standard `O_APPEND` is only atomic for small writes (typically <4KB or PIPE_BUF). Our context capabilities can exceed this easily.

- **Risk**: Interleaved JSON lines (corrupting the log).
- **Solution**: Must use file locking.
- **Implementation**: Python's `fcntl.flock` is standard on macOS/Linux.
- **Trade-off**: Slightly slower, but safety is paramount for an audit log.

### Logging Schema

We need a `JSONL` format where each line is a complete event.

```json
{
  "timestamp": "ISO8601",
  "run_id": "UUID-v4",
  "event_type": "context_injection",
  "workflow": "plan",
  "objective": "Phase 1 research",
  "selected_skills": ["skill_id_1", "skill_id_2"],
  "full_prompt_fragment": "...(the full text)...",
  "fragment_length": 15420,
  "source_integrity": {
    "skill_id_1": "OK",
    "skill_id_2": "TRUNCATED" // if we implement internal checking
  }
}
```

### Verification Logic

A verifier script (`gsd_verify_log.py`) can:

1. Parse the JSONL.
2. For each entry, load current `SKILLS.md`.
3. Extract the "truth" text for the selected skills.
4. Compare `truth` vs `log.full_prompt_fragment`.
5. Report any mismatch.

## Decisions Made

| Decision    | Choice                  | Rationale                                  |
| ----------- | ----------------------- | ------------------------------------------ |
| **Locking** | `fcntl.flock`           | Zero external dependencies, safe on macOS. |
| **Format**  | JSONL                   | Easy to stream-process and append.         |
| **Storage** | `.gsd/logs/audit.jsonl` | Centralized location.                      |

## Patterns to Follow

- **Context Manager**: Use a `with` block for safe locking/unlocking.
- **Lazy Loading**: Don't load the log file into memory; append only.

## Risks

- **Disk Space**: Logs can grow fast. Mitigation: `log_rotate` or manual truncation? For now, user manages it.

## Ready for Planning

- [x] Questions answered
- [x] Approach selected
- [x] Dependencies identified (std libs: `fcntl`, `json`, `uuid`)
