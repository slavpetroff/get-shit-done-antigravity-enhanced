# SKILLS.md — Local Agent Intelligence

> **Status**: `INITIALIZED`
> **Discovery Mode**: `AUTO`

This registry contains specialized skills discovered in `.agent/skills/`. Each skill provides domain-specific knowledge and optimized prompts for Antigravity.

---

## Technical Details
This file is both a human-readable inventory and a machine-readable registry. GSD uses the `<gsd_registry>` block below for automated tool selection and prompt injection.

---

## GSD Codebase Mapper
- **ID**: `codebase-mapper`
- **Confidence**: `0.5`

### Description
Analyzes existing codebases to understand structure, patterns, and technical debt

---

## Context Health Monitor
- **ID**: `context-health-monitor`
- **Confidence**: `1.0`

### Description
Monitors context complexity and triggers state dumps before quality degrades

### Purpose
Prevent "Context Rot" — the quality degradation that occurs as the agent processes more information in a single session.

### Activation
The agent should self-monitor for these warning signs:

### Warning Signs

| Signal | Threshold | Action |
|--------|-----------|--------|
| Repeated debugging | 3+ failed attempts | Trigger state dump |
| Going in circles | Same approach tried twice | Stop and reassess |
| Confusion indicators | "I'm not sure", backtracking | Document uncertainty |
| Session length | Extended back-and-forth | Recommend `/pause` |

### Behavior & Constraints
### Rule 1: The 3-Strike Rule

If debugging the same issue fails 3 times:

1. **STOP** attempting fixes
2. **Document** in `.gsd/STATE.md`:
   - What was tried
   - What errors occurred
   - Current hypothesis
3. **Recommend** user start fresh session
4. **Do NOT** continue with more attempts

### Rule 2: Circular Detection

If the same approach is being tried again:

1. **Acknowledge** the repetition
2. **List** what has already been tried
3. **Propose** a fundamentally different approach
4. **Or** recommend `/pause` for fresh perspective

### Rule 3: Uncertainty Logging

When uncertain about an approach:

1. **State** the uncertainty clearly
2. **Document** in `.gsd/DECISIONS.md`:
   - The uncertain decision
   - Why it's uncertain
   - Alternatives considered
3. **Ask** user for guidance rather than guessing

---

## GSD Debugger
- **ID**: `debugger`
- **Confidence**: `0.5`

### Description
Systematic debugging with persistent state and fresh context advantages

---

## Empirical Validation
- **ID**: `empirical-validation`
- **Confidence**: `0.5`

### Description
Requires proof before marking work complete — no "trust me, it works"

---

## GSD Executor
- **ID**: `executor`
- **Confidence**: `1.0`

### Description
Executes GSD plans with atomic commits, deviation handling, checkpoint protocols, and state management

### Behavior & Constraints
### Step 1: Load Project State

Before any operation, read project state:

```powershell
Get-Content ".gsd/STATE.md" -ErrorAction SilentlyContinue
```

**If file exists:** Parse and internalize:
- Current position (phase, plan, status)
- Accumulated decisions (constraints on this execution)
- Blockers/concerns (things to watch for)

**If file missing but .gsd/ exists:** Reconstruct from existing artifacts.

**If .gsd/ doesn't exist:** Error — project not initialized.

### Step 2: Load Plan

Read the plan file provided in your prompt context.

Parse:
- Frontmatter (phase, plan, type, autonomous, wave, depends_on)
- Objective
- Context files to read
- Tasks with their types
- Verification criteria
- Success criteria

### Step 3: Determine Execution Pattern

**Pattern A: Fully autonomous (no checkpoints)**
- Execute all tasks sequentially
- Create SUMMARY.md
- Commit and report completion

**Pattern B: Has checkpoints**
- Execute tasks until checkpoint
- At checkpoint: STOP and return structured checkpoint message
- Fresh continuation agent resumes

**Pattern C: Continuation (spawned to continue)**
- Check completed tasks in your prompt
- Verify those commits exist
- Resume from specified task

### Step 4: Execute Tasks

For each task:

1. **Read task type**

2. **If `type="auto"`:**
   - Work toward task completion
   - If CLI/API returns authentication error → Handle as authentication gate
   - When you discover additional work not in plan → Apply deviation rules
   - Run the verification
   - Confirm done criteria met
   - **Commit the task** (see Task Commit Protocol)
   - Track completion and commit hash for Summary

3. **If `type="checkpoint:*"`:**
   - STOP immediately
   - Return structured checkpoint message
   - You will NOT continue — a fresh agent will be spawned

4. Run overall verification checks
5. Document all deviations in Summary

---

---

## GSD Plan Checker
- **ID**: `plan-checker`
- **Confidence**: `0.5`

### Description
Validates plans before execution to catch issues early

---

## GSD Planner
- **ID**: `planner`
- **Confidence**: `1.0`

### Description
Creates executable phase plans with task breakdown, dependency analysis, and goal-backward verification

### When to Use
### When to Use TDD Plans

Detect TDD fit when:
- Complex business logic with edge cases
- Financial calculations
- State machines
- Data transformation pipelines
- Input validation rules

### TDD Plan Structure

```markdown
---
phase: {N}
plan: {M}
type: tdd
wave: {W}
---

# TDD Plan: {Feature}

---

## GSD Verifier
- **ID**: `verifier`
- **Confidence**: `0.5`

### Description
Validates implemented work against spec requirements with empirical evidence

---


<gsd_registry>
    <!-- MACHINE-READABLE REGISTRY -->
    <item id="codebase-mapper" confidence="0.5">
        <name>GSD Codebase Mapper</name>
        <path>.agent/skills/codebase-mapper/SKILL.md</path>
        <description>Analyzes existing codebases to understand structure, patterns, and technical debt</description>
    </item>
    <item id="context-health-monitor" confidence="1.0">
        <name>Context Health Monitor</name>
        <path>.agent/skills/context-health-monitor/SKILL.md</path>
        <description>Monitors context complexity and triggers state dumps before quality degrades</description>
    </item>
    <item id="debugger" confidence="0.5">
        <name>GSD Debugger</name>
        <path>.agent/skills/debugger/SKILL.md</path>
        <description>Systematic debugging with persistent state and fresh context advantages</description>
    </item>
    <item id="empirical-validation" confidence="0.5">
        <name>Empirical Validation</name>
        <path>.agent/skills/empirical-validation/SKILL.md</path>
        <description>Requires proof before marking work complete — no "trust me, it works"</description>
    </item>
    <item id="executor" confidence="1.0">
        <name>GSD Executor</name>
        <path>.agent/skills/executor/SKILL.md</path>
        <description>Executes GSD plans with atomic commits, deviation handling, checkpoint protocols, and state management</description>
    </item>
    <item id="plan-checker" confidence="0.5">
        <name>GSD Plan Checker</name>
        <path>.agent/skills/plan-checker/SKILL.md</path>
        <description>Validates plans before execution to catch issues early</description>
    </item>
    <item id="planner" confidence="1.0">
        <name>GSD Planner</name>
        <path>.agent/skills/planner/SKILL.md</path>
        <description>Creates executable phase plans with task breakdown, dependency analysis, and goal-backward verification</description>
    </item>
    <item id="verifier" confidence="0.5">
        <name>GSD Verifier</name>
        <path>.agent/skills/verifier/SKILL.md</path>
        <description>Validates implemented work against spec requirements with empirical evidence</description>
    </item>
</gsd_registry>
