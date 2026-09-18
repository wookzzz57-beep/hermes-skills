# Interruption / Resume Demo

This fixture demonstrates the smallest useful promise of Hermes Durable:

> a fresh coding-agent session can recover the authorized task, verified progress, and next action from repository state without replaying the original chat.

## 1. Start the task

```bash
hermes-durable init checkout-17 \
  --objective "Fix duplicate checkout submission without changing the public API" \
  --scope "src/checkout" \
  --non-goal "Refactor payment providers" \
  --accept "duplicate-submit regression test passes" \
  --accept "existing checkout tests still pass"
```

## 2. Do one verified step, then checkpoint

Assume the first session reproduced the bug and added a regression test, but was interrupted before implementing the fix.

```bash
hermes-durable evidence checkout-17 \
  --kind test \
  --summary "Regression test reproduces duplicate submit before the fix" \
  --command "pytest tests/checkout/test_duplicate_submit.py -q" \
  --result "1 failed as expected"

hermes-durable checkpoint checkout-17 \
  --stage implementation \
  --completed "reproduced duplicate submit" \
  --completed "added regression test" \
  --next-action "Guard the submit path with the existing in-flight request state"
```

At this point the original chat/process can disappear.

## 3. Resume in a fresh session

Give the new coding agent this instruction:

```text
Read .agent/tasks/checkout-17/task.json, checkpoint.json, and evidence.jsonl.
Resume only from the durable next_action. Do not repeat completed side effects.
Do not declare completion until every acceptance criterion has fresh evidence.
```

The sample state in this directory shows what that fresh session should recover:

- the exact authorized objective;
- the allowed scope and explicit non-goal;
- what was already completed;
- the next concrete action;
- observable evidence from the prior session.

## 4. Finish and verify

After implementing the fix, append fresh test evidence and run:

```bash
hermes-durable verify checkout-17
```

The v0.1 structural gate proves that a task contract, checkpoint, and non-empty evidence ledger exist. Issue #1 tracks criterion-level evidence coverage for v0.2.

## Why this matters

Without durable state, a replacement agent usually has to trust a summary, replay a long conversation, or rediscover work. The repository state here is intentionally small enough to inspect, diff, review, and hand off.
