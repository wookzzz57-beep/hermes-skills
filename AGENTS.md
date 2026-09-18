# AGENTS.md

## Repository purpose

Hermes Durable is a small, provider-neutral reliability layer for coding agents. It should remain useful with Codex and other agents without becoming a general agent runtime.

## Layout

- `skills/` — reusable Agent Skills. Each skill has a concise `SKILL.md`.
- `src/hermes_durable/` — zero-runtime-dependency Python CLI.
- `tests/` — CLI regression tests.
- `examples/` — inspectable maintenance and recovery examples.
- `docs/` — roadmap and supporting documentation.

## Required checks

Before treating a code or skill change as complete, run:

```bash
python scripts/validate_skills.py
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
```

## Engineering rules

- Keep Python runtime dependencies at zero unless a dependency has a concrete, reviewed benefit.
- Preserve provider-neutral task state; do not require a vendor session ID for recovery.
- Treat chat/session context as cache, not canonical task state.
- Persist state with explicit schemas and backwards-compatible changes where practical.
- Do not execute commands stored in task or evidence files.
- Do not store credentials, secrets, customer data, or access tokens in durable task state.
- Reject unsafe task IDs or paths rather than normalizing them silently.
- Prefer atomic replacement for structured state and append-only evidence records.
- Keep `SKILL.md` files short enough to load only the workflow an agent needs.

## Pull requests

A PR should explain the concrete reliability failure or maintainer pain it addresses. Code changes need tests. Skill changes need a valid trigger description, explicit boundaries, and a verification/completion section where applicable.

## Code Review Rules

- Flag changes that let a worker declare success without observable verification.
- Flag state updates that can corrupt or overwrite the last known-good checkpoint on interruption.
- Flag provider-specific coupling in the core task/checkpoint/evidence contract unless isolated behind an adapter.
- Flag any path from repository-controlled task content to implicit command execution.
- Flag examples or documentation that overstate guarantees not implemented by the CLI.

## Definition of done

Implementation is not enough. The relevant checks above must pass, documentation must match behavior, and remaining limitations must stay explicit.
