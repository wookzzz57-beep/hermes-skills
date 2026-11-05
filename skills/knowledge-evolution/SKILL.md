---
name: knowledge-evolution
description: Distill evidenced task outcomes into bounded daily knowledge and independently tested Skill or automation improvement candidates; use when reviewing recurring work, failed tasks, accepted corrections, or weekly capability promotion without touching production automatically.
---

# Knowledge Evolution

Improve **accepted result quality and reliability**, not the number of notes or versions. An observation is not a validated capability; a passing text check is not a production release.

## Start: recover the contract

1. Read the active task objective, current schedule, local authority order, canonical knowledge constitution, previous checkpoints, and relevant source/evidence references.
2. Identify the real system of record, permitted read/write path, current release/version, ownership, and forbidden surfaces. This Skill never grants new access or changes a task's schedule.
3. Snapshot source coverage, source timestamps, baseline Git commit/dirty set where accessible, and the last **independently accepted** state. Missing access is `NOT_ACCESSIBLE`, never inferred from memories or previous assistant claims.
4. Keep the currently deployed and the intended future control architectures distinct. Do not assume an intended executor has been deployed.

## Daily: distill and detect

- Analyze the task's existing daily time window; add only genuine new evidence using stable IDs. Keep the original date for late-arriving evidence.
- Distill at most five high-value, source-linked learnings. Separate `FACT` from `INFERENCE` and `SOLVED` from `PROVISIONAL`, `UNRESOLVED`, and `BLOCKED`.
- Compare accepted results, failures, user corrections, regressions, and repeated manual work. A repeatable failure or correction may yield **at most one** priority improvement proposal per run; no evidence yields `NONE`.
- Identify what should change, the smallest scoped delta, what must stay unchanged, a measurable expected benefit, and conditions that would falsify the improvement.
- Do not copy complete conversations, secrets, or raw traces into long-term knowledge.

## Weekly: governance and experiment

1. Audit coverage for all required daily artifacts; preserve gaps and contradiction markers instead of filling missing days.
2. Group candidates by root cause and reuse scope; merge duplicates, supersede obsolete claims, and explicitly reject unsupported generalizations.
3. Compare candidate behavior with the frozen baseline on matching inputs. Inspect trigger precision, negative cases, side effects, outputs, evidence handling, and recovery behavior.
4. For each high-value Skill or automation candidate, prepare: minimal patch/diff; changelog; original failure fixture; positive, negative, regression, and cross-context transfer fixtures; expected quality metric; rollback instructions.
5. Run static checks and safe replay/shadow evaluation **only through an actually accessible, authorized executor**. Do not treat a simulated or unavailable test as a pass. Record command/run ID, build or commit SHA, test output, and independent review where available.
6. Rank no more than three experiments by accepted-result quality, reliability, evidence completeness, recovery, cost, then latency. Saving tokens is not a gain if quality falls.

## Candidate and promotion contract

Record each proposal with these fields: `candidate_id`, `source_ids`, `event_date`, `base_version`, `proposed_version`, `affected_skill_or_automation`, `problem`, `scope`, `non_goals`, `evidence`, `baseline_metric`, `expected_metric`, `patch_ref`, `fixture_refs`, `static_result`, `replay_result`, `regression_result`, `transfer_result`, `independent_verifier`, `risk_level`, `rollback_ref`, `lifecycle`, `owner`, `resume_point`.

- `OBSERVED` / `CANDIDATE`: claim or draft exists; no permission to replace an active asset.
- `VERIFIED_CANDIDATE`: trustworthy source, accepted original result, static checks and applicable bounded replay/regression/transfer evidence are attached; any required independent verification passed.
- `RETAINED`: a separately approved, safely persisted knowledge or governance artifact with readback; active executable Skill promotion requires explicit authorization under the governing contract. Never infer deployment from a PR, commit, or artifact creation.
- `MERGED` / `SUPERSEDED` / `REJECTED` / `QUARANTINED`: preserve the reason and evidence; stop repeating failed candidates without new evidence.

Treat a semantics-changing Skill, guard, judge, or detector as **new behavior**: prior validation evidence cannot automatically carry over.

## Authorization and side-effect policy

- **L0**: Draft, evaluate and, only within an authorized knowledge write scope, persist low-risk knowledge or non-executable SOP deltas with idempotent IDs and readback.
- **L1**: For an executable Skill, create an isolated candidate/PR, run bounded tests and prepare a rollback. Do not auto-activate or overwrite the last-known-good release.
- **L2**: Human decision required for production deployment, money/pricing, secrets/permissions, irreversible deletion, core runtime and account changes, or any change without a demonstrated rollback.
- Never change unrelated files, history, queues, leases, or project runtime state. Never use `git add .`; stage only validated, owned paths. Never substitute an unauthorized storage location when the canonical destination is unreachable.

## Acceptance and failure behavior

An execution is `PASS` only when its required evidence, permitted persistence, post-write readback, links, idempotency, and selective Git finalization all pass. Otherwise distinguish:

- `ANALYSIS_ONLY`: conclusions made, no verified write.
- `CANDIDATE_READY`: proposal and tested diff exist; production unchanged.
- `PERSISTENCE_BLOCKED`: canonical destination unavailable or write authority unproven.
- `PERSISTED_UNCOMMITTED`: file readback passed but required Git finalization failed.
- `REGRESSION_FAILED`: new behavior breaks a frozen accepted case; stop promotion and preserve the previous release.
- `PARTIAL` / `UNVERIFIED`: required inputs or checks unavailable.

Emit one concise handoff: `period`, `coverage`, `source_ids`, `candidate_ids`, `tested_candidate_ids`, `retained_ids`, `rejected_ids`, `changed_paths`, `base_sha`, `result_sha`, `evidence_refs`, `persistence_state`, `production_unchanged`, `open_loops`, `resume_point`, `next_test`.

Never say a Skill was installed, an Obsidian vault updated, or a live workflow improved unless independently observable evidence confirms that exact effect.
