---
phase: 14
wave: 1
gap_closure: false
---

# Phase 14 Execution Plan: Kaizen Loop

## Objective

Implement a self-correction loop where the agent proposes improvements to its own skills and workflows upon task failure.

## Context

- **Trigger**: Automatic on verification failure.
- **Guardrails**: Reviewer Sub-Agent + Explicit User Confirmation.
- **Scope**: Skills and Workflows.

## Tasks

<task type="auto">
<name>Create Proposal Script</name>
<files>scripts/propose_improvement.py</files>
<action>
Create `scripts/propose_improvement.py`.
- Input: Task Objective, Failed Verification Output, Context.
- Logic:
  1. Identify which skill/workflow was active (or should have been).
  2. Generate a diagnosis (What failed, Why).
  3. Generate a "patch" or suggested edit for the skill/workflow file.
  4. Output JSON: `{ "diagnosis": "...", "target_file": "...", "suggested_change": "..." }`
</action>
<verify>test -f scripts/propose_improvement.py</verify>
<done>Script created.</done>
</task>

<task type="auto">
<name>Create Reviewer Script</name>
<files>scripts/review_proposal.py</files>
<action>
Create `scripts/review_proposal.py`.
- Input: Output from `propose_improvement.py`.
- Logic:
  1. Load **Reviewer Persona**.
  2. Validate if the change is safe and aligns with architectural rules.
  3. Output: "APPROVED" or "REJECTED" with reason.
</action>
<verify>test -f scripts/review_proposal.py</verify>
<done>Reviewer script created.</done>
</task>

<task type="auto">
<name>Integrate into Execute Workflow</name>
<files>.agent/workflows/execute.md</files>
<action>
Modify `/execute` to handle verification failure:
- Capture exit code of `<verify>`.
- If fail:
  1. Run `scripts/propose_improvement.py`.
  2. Run `scripts/review_proposal.py`.
  3. Display proposal to user.
  4. Prompt: "Apply improvement? [y/N]"
  5. If yes, apply change to the skill/workflow file.
</action>
<verify>grep "propose_improvement.py" .agent/workflows/execute.md</verify>
<done>Workflow updated with Kaizen loop.</done>
</task>

<task type="auto">
<name>Sync Templates</name>
<files>.gsd/templates/scripts/, .gsd/templates/.agent/workflows/</files>
<action>
Sync the new scripts and workflow to templates.
</action>
<verify>test -f .gsd/templates/scripts/propose_improvement.py</verify>
<done>Templates synced.</done>
</task>
