# Contributing

Contributions are welcome when they improve a reproducible agent-maintenance workflow.

## Good contributions

- a failure case that causes coding agents to lose task state or claim completion too early;
- a smaller, clearer task/checkpoint/evidence contract;
- cross-platform installation improvements;
- deterministic verification helpers;
- examples grounded in real repository maintenance.

## Pull requests

1. Keep one conceptual change per PR.
2. Explain the failure mode or maintainer pain being solved.
3. Add or update tests when code changes.
4. Run:
   ```bash
   python scripts/validate_skills.py
   PYTHONPATH=src python -m unittest discover -s tests -v
   ```
5. Avoid provider-specific behavior in the core contract unless it is isolated behind an adapter.

By contributing, you agree that your contribution is licensed under the MIT License.
