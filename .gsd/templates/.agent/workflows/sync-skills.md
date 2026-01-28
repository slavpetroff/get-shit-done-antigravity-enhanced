---
description: Discover and index project skills and MCP servers
---

# /sync-skills Workflow

<objective>
Scan the project for local skills and global MCP configurations to keep the registries updated.
This ensures the AI agent has access to the latest "When to use" and "Behavior Rules" for all project tools.
</objective>

<process>

## 1. Run Discovery Engine

Execute the synchronization script:

**Bash/Zsh:**

```bash
python3 scripts/gsd_sync.py --output json
python3 scripts/categorize_skills.py
```

## 2. Verify Output

Check `.gsd/SKILLS.md` and `.gsd/MCPS.md` to ensure they have been updated within the `<gsd_registry>` blocks.

## 3. Position the Agent

Recommended next action if new skills are discovered:
• Review `SKILLS.md` to confirm documentation is complete.
• Run `/resume` to ensure your session context is optimized.

</process>
