# Hermes Durable Skills

[![CI](https://github.com/wookzzz57-beep/hermes-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/wookzzz57-beep/hermes-skills/actions/workflows/ci.yml)

**Durable task state, checkpoint/resume, and evidence gates for coding agents.**

Works with Codex, Claude Code, Cursor, Hermes Agent, and any agent that can read `SKILL.md` and repository files.

> Chat is working cache. Repository state is durable. An agent saying “done” is not acceptance evidence.

[中文说明](./README.zh-CN.md)

## Why this exists

Coding agents are fast inside one session. Real maintenance work is harder:

- a task spans multiple sessions or model limits;
- the agent forgets scope and starts improving unrelated code;
- a process restarts and completed side effects get repeated;
- the worker reports success, but nobody can prove the acceptance criteria passed;
- another maintainer or agent must resume without replaying a long chat.

Hermes Durable adds a small, provider-neutral reliability layer instead of another agent runtime.

## The three skills

| Skill | Purpose |
| --- | --- |
| `durable-task` | Freeze objective, scope, non-goals, constraints, acceptance criteria, and stop conditions before risky or multi-step work. |
| `checkpoint-resume` | Persist the current lane and resume after context loss, interruption, provider switching, or human handoff. |
| `evidence-gate` | Map acceptance criteria to fresh tests, commands, diffs, artifacts, or manual evidence before declaring completion. |

These skills follow the `SKILL.md` structure used by modern coding-agent skill systems.

## 60-second demo

```bash
git clone https://github.com/wookzzz57-beep/hermes-skills.git
cd hermes-skills
python -m pip install .

hermes-durable init fix-42 \
  --objective "Fix checkout regression without changing the public API" \
  --scope "src/checkout" \
  --non-goal "Refactor payment providers" \
  --accept "checkout unit tests pass" \
  --accept "checkout smoke test passes"

hermes-durable checkpoint fix-42 \
  --stage implementation \
  --completed "isolated failing test" \
  --next-action "patch the tax rounding branch"

hermes-durable evidence fix-42 \
  --kind test \
  --summary "checkout tests passed" \
  --command "pytest tests/checkout -q" \
  --result "exit 0"

hermes-durable verify fix-42
```

Durable state lives with the repository:

```text
.agent/tasks/fix-42/
├── task.json
├── checkpoint.json
└── evidence.jsonl
```

A new session can read those files and continue the actual task instead of reconstructing intent from chat history.

**Try the full interruption/resume walkthrough:** [examples/interruption-resume](./examples/interruption-resume/README.md)

## Install the skills

Clone once:

```bash
git clone https://github.com/wookzzz57-beep/hermes-skills.git
```

For Codex:

```bash
mkdir -p ~/.codex/skills
cp -R hermes-skills/skills/durable-task ~/.codex/skills/
cp -R hermes-skills/skills/checkpoint-resume ~/.codex/skills/
cp -R hermes-skills/skills/evidence-gate ~/.codex/skills/
```

For Hermes Agent, copy the same skill folders to `~/.hermes/skills/`. Other `SKILL.md`-compatible clients can use their normal skill directories.

## Maintainer use cases

### Interrupted release

Persist release criteria and current stage before the release starts. If the terminal, agent session, or provider dies, resume from the last durable checkpoint without repeating already-proven effects.

### PR maintenance

Keep a narrow task contract for a bugfix or dependency update. The worker can change, but scope and acceptance criteria remain stable.

### Evidence-first acceptance

Record tests, build output, diffs, artifact hashes, or manual checks in an append-only JSONL ledger. A worker's narrative is useful context, not proof.

## Design principles

- **Capability before complexity** — use existing coding agents; add only the missing reliability layer.
- **Durable state before long-chat memory** — important task state survives session loss.
- **Evidence before completion** — completion is an acceptance decision, not a model phrase.
- **Resume instead of replay** — continue from the next verified action.
- **Provider-neutral core** — no task should depend on one vendor's session format.
- **No secrets in state** — task packets and evidence are repository artifacts.

## CLI

```text
hermes-durable init <task_id> ...
hermes-durable checkpoint <task_id> ...
hermes-durable evidence <task_id> ...
hermes-durable verify <task_id>
hermes-durable status <task_id>
```

The CLI has no runtime dependencies beyond Python 3.10+.

## Project status

**v0.1.0** — usable foundation. The next milestone focuses on maintainer automation: PR verification, release workflows, issue-triage templates, and interoperability. See [ROADMAP](./docs/ROADMAP.md).

The reliability patterns are adapted from a larger private agent-control system, but this repository is a standalone public implementation with no dependency on private infrastructure.

## Contributing

Issues and PRs that reproduce real maintenance failures are especially useful. See [CONTRIBUTING.md](./CONTRIBUTING.md) and [SECURITY.md](./SECURITY.md).

## License

MIT

If this project fixes a real maintenance failure for you, a GitHub star helps other maintainers discover it.
