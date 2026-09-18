---
name: checkpoint-resume
description: Checkpoint or resume long-running coding-agent work across context resets, process interruption, provider switching, or human handoff without replaying the whole chat or repeating completed side effects.
---

# Checkpoint Resume

Persist the minimum state needed to continue correctly after an interruption.

## Checkpoint

1. Read the active task contract.
2. Record:
   - current stage
   - completed steps that have evidence
   - unresolved blockers
   - one concrete next action
   - relevant artifact or commit references
3. Prefer `hermes-durable checkpoint` when available.
4. Write checkpoints atomically. Never destroy the last known-good checkpoint before the replacement is complete.
5. Do not call a step complete only because the current agent remembers doing it.

## Resume

1. Read `task.json`, then `checkpoint.json`, then the evidence ledger.
2. Reconstruct the current lane from durable state before reading old chat history.
3. Confirm that referenced files, commits, or test outputs still exist when they materially affect the next action.
4. Treat side effects as already completed only when durable evidence or repository state proves they occurred.
5. Continue from `next_action`; do not restart the whole plan by default.
6. If durable state conflicts with current repository reality, stop and surface the conflict instead of guessing.

## Handoff

Keep the handoff provider-neutral. A different coding agent should be able to resume the task from repository state alone.
