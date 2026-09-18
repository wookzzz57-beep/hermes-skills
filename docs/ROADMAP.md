# Roadmap

Hermes Durable is intentionally small. The goal is not another agent runtime; it is a portable reliability layer around runtimes people already use.

## v0.1 — shipped

- provider-neutral task contract
- checkpoint/resume skill
- evidence-first acceptance skill
- zero-runtime-dependency Python CLI
- CI validation and tests

## v0.2 — maintainer workflows

- GitHub Action that verifies task/evidence structure on pull requests
- release checklist adapter
- issue-triage task templates
- criterion-to-evidence report output
- examples for Codex and other coding agents

## v0.3 — interoperability

- import/export for common handoff formats
- idempotency/effect records for maintenance automation
- optional signatures/checksums for evidence artifacts
- benchmark fixtures for interruption and resume behavior

## Non-goals

- replacing Codex, Claude Code, Cursor, Hermes Agent, or other coding runtimes
- remote shell execution
- storing credentials
- an always-on cloud control plane
