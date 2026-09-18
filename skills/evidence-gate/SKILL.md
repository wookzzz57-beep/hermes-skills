---
name: evidence-gate
description: Verify whether coding, maintenance, migration, release, or agent-generated work is actually complete by mapping each acceptance criterion to fresh observable evidence instead of trusting the worker's summary.
---

# Evidence Gate

Worker output is a claim. Acceptance requires evidence.

## Verification Loop

1. Load the active task contract and current acceptance criteria.
2. Build a criterion-to-evidence map.
3. Prefer deterministic evidence first:
   - tests and linters
   - build output
   - repository diff or file inspection
   - generated artifacts and checksums
   - reproducible commands
4. Use manual or model-based review only where deterministic checks cannot observe the requirement.
5. Record each meaningful result in the evidence ledger. Prefer `hermes-durable evidence` when available.
6. Run `hermes-durable verify <task_id>` as a structural gate when the CLI is installed.
7. Report unmet criteria explicitly. Do not downgrade a failure to a warning merely to close the task.

## Freshness

Evidence should reflect the implementation being accepted. Re-run checks affected by later edits.

## Independence

For high-impact work, prefer an independent verifier or fresh review pass rather than relying only on the same worker that made the change.

## Completion Contract

Declare completion only when:
- the objective remains the same task the user authorized,
- all required acceptance criteria have supporting evidence,
- no stop condition is active,
- the durable checkpoint reflects the final state and no hidden remainder is being treated as done.
