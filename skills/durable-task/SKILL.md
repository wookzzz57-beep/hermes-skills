---
name: durable-task
description: Create a durable task contract before multi-step coding, maintenance, migration, or release work where scope drift, context loss, or ambiguous completion criteria would be costly.
---

# Durable Task

Treat chat context as working memory, not the source of truth for a long-running task.

## Workflow

1. Inspect only the repository context needed to understand the requested outcome.
2. Freeze a compact task contract with:
   - stable `task_id`
   - objective
   - in-scope work
   - explicit non-goals
   - constraints and authorization boundaries
   - testable acceptance criteria
   - stop conditions
3. Prefer the bundled `hermes-durable init` command when available. Otherwise persist the same fields under `.agent/tasks/<task_id>/task.json`.
4. Do not silently rewrite acceptance criteria to match an implementation that already exists. If the contract must change, record the change before continuing.
5. Execute the smallest next step that advances one or more acceptance criteria.
6. After a meaningful unit of work, persist a checkpoint with the completed steps and one concrete next action.
7. Record observable evidence separately from the agent's own summary.

## Boundaries

- Do not create durable state for tiny, single-step edits that can be safely completed and verified in the current session.
- Do not use the task contract to expand the user's authorization.
- Do not mark a task complete merely because an implementation command exited successfully.
- Keep provider-specific session IDs optional; the durable task must remain understandable without one.

## Completion

A task is ready for completion review only when its current acceptance criteria can be mapped to fresh evidence. Use the `evidence-gate` skill for that review.
