from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from hermes_durable.cli import main


class DurableCliTests(unittest.TestCase):
    def test_init_evidence_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rc = main([
                "--root", str(root),
                "init", "T-1",
                "--objective", "Ship a tested change",
                "--scope", "src/",
                "--accept", "unit tests pass",
            ])
            self.assertEqual(rc, 0)
            task = json.loads((root / ".agent/tasks/T-1/task.json").read_text())
            self.assertEqual(task["status"], "ready")

            self.assertEqual(main([
                "--root", str(root),
                "evidence", "T-1",
                "--kind", "test",
                "--summary", "unit tests passed",
                "--command", "python -m unittest",
                "--result", "exit 0",
            ]), 0)

            self.assertEqual(main([
                "--root", str(root),
                "verify", "T-1",
            ]), 0)

    def test_verify_fails_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main([
                "--root", str(root),
                "init", "T-2",
                "--objective", "Do work",
                "--accept", "observable result exists",
            ]), 0)
            self.assertEqual(main([
                "--root", str(root),
                "verify", "T-2",
            ]), 1)

    def test_rejects_unsafe_task_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main([
                "--root", tmp,
                "init", "../escape",
                "--objective", "Do work",
                "--accept", "done",
            ]), 2)


if __name__ == "__main__":
    unittest.main()
