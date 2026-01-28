# Library Intelligence Registry

> **Status**: Experimental (Milestone v2.0)

This directory contains structured "Library Intelligence" — curated knowledge about specific frameworks and libraries used in this project.

## Purpose

Unlike **Skills** (which teach _how_ to do a task), **Library Intelligence** provides _facts_ and _constraints_ about a specific tool (e.g., React, FastAPI).

Each entry contains:

- **Anti-Patterns**: What NOT to do.
- **Idioms**: The "correct" way to use the library in this project.
- **Best Practices**: Performance, security, and architectural guidelines.

## Structure

Files are organized by category:

- `frontend/`: UI frameworks (React, Tailwind, etc.)
- `backend/`: Server frameworks (FastAPI, Django, Node, etc.)
- `security/`: Auth and crypto libs.
- `devops/`: Infrastructure tools (Docker, AWS).
- `ai/`: AI/ML frameworks (LangChain, OpenAI).

## Population

This registry is populated **dynamically** via the `/sync-libs` workflow.
It scans `package.json` and `pyproject.toml` to identify high-value libraries and fetches intelligence from the web.
