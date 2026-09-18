from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def safe_task_id(value: str) -> str:
    if not TASK_ID_RE.fullmatch(value):
        raise ValueError("task_id must be 1-80 chars: letters, digits, dot, underscore, hyphen")
    return value


def task_dir(root: Path, task_id: str) -> Path:
    return root / ".agent" / "tasks" / safe_task_id(task_id)


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    target = task_dir(root, args.task_id)
    task_path = target / "task.json"
    if task_path.exists():
        print(f"ERROR task already exists: {task_path}", file=sys.stderr)
        return 2
    packet = {
        "schema": "hermes-durable/task-v1",
        "task_id": args.task_id,
        "objective": args.objective.strip(),
        "scope": args.scope or [],
        "non_goals": args.non_goal or [],
        "constraints": args.constraint or [],
        "acceptance": args.accept or [],
        "stop_conditions": args.stop_condition or [],
        "status": "ready",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    if not packet["objective"]:
        print("ERROR objective cannot be empty", file=sys.stderr)
        return 2
    if not packet["acceptance"]:
        print("ERROR at least one --accept criterion is required", file=sys.stderr)
        return 2
    atomic_json(task_path, packet)
    atomic_json(target / "checkpoint.json", {
        "schema": "hermes-durable/checkpoint-v1",
        "task_id": args.task_id,
        "stage": "ready",
        "completed_steps": [],
        "next_action": "Start the first accepted implementation step.",
        "updated_at": now_iso(),
    })
    (target / "evidence.jsonl").touch(exist_ok=True)
    print(target)
    return 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    target = task_dir(root, args.task_id)
    task_path = target / "task.json"
    if not task_path.exists():
        print("ERROR task does not exist", file=sys.stderr)
        return 2
    checkpoint = {
        "schema": "hermes-durable/checkpoint-v1",
        "task_id": args.task_id,
        "stage": args.stage,
        "completed_steps": args.completed or [],
        "next_action": args.next_action.strip(),
        "updated_at": now_iso(),
    }
    if not checkpoint["next_action"]:
        print("ERROR --next-action cannot be empty", file=sys.stderr)
        return 2
    atomic_json(target / "checkpoint.json", checkpoint)
    task = load_json(task_path)
    task["status"] = args.stage
    task["updated_at"] = now_iso()
    atomic_json(task_path, task)
    print(target / "checkpoint.json")
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    target = task_dir(root, args.task_id)
    if not (target / "task.json").exists():
        print("ERROR task does not exist", file=sys.stderr)
        return 2
    record = {
        "schema": "hermes-durable/evidence-v1",
        "task_id": args.task_id,
        "timestamp": now_iso(),
        "kind": args.kind,
        "summary": args.summary.strip(),
    }
    if args.command:
        record["command"] = args.command
    if args.result:
        record["result"] = args.result
    if args.artifact:
        record["artifacts"] = args.artifact
    if not record["summary"]:
        print("ERROR --summary cannot be empty", file=sys.stderr)
        return 2
    evidence_path = target / "evidence.jsonl"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    with evidence_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    print(evidence_path)
    return 0


def verify_task(root: Path, task_id: str) -> tuple[bool, list[str]]:
    target = task_dir(root, task_id)
    failures: list[str] = []
    task_path = target / "task.json"
    checkpoint_path = target / "checkpoint.json"
    evidence_path = target / "evidence.jsonl"
    if not task_path.exists():
        return False, ["task.json missing"]
    task = load_json(task_path)
    if not task.get("objective"):
        failures.append("objective missing")
    acceptance = task.get("acceptance")
    if not isinstance(acceptance, list) or not acceptance:
        failures.append("acceptance criteria missing")
    if not checkpoint_path.exists():
        failures.append("checkpoint.json missing")
    else:
        checkpoint = load_json(checkpoint_path)
        if not checkpoint.get("next_action"):
            failures.append("checkpoint next_action missing")
    if not evidence_path.exists() or not evidence_path.read_text(encoding="utf-8").strip():
        failures.append("evidence ledger empty")
    return not failures, failures


def cmd_verify(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ok, failures = verify_task(root, args.task_id)
    if ok:
        print(f"PASS {args.task_id}: task contract, checkpoint, and evidence are present")
        return 0
    print(f"FAIL {args.task_id}", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    return 1


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    target = task_dir(root, args.task_id)
    for filename in ("task.json", "checkpoint.json"):
        path = target / filename
        if path.exists():
            print(f"## {filename}")
            print(path.read_text(encoding="utf-8").rstrip())
    evidence_path = target / "evidence.jsonl"
    if evidence_path.exists():
        lines = [line for line in evidence_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        print(f"## evidence.jsonl ({len(lines)} records)")
        for line in lines[-5:]:
            print(line)
    if not target.exists():
        print("ERROR task does not exist", file=sys.stderr)
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hermes-durable")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a durable task contract")
    p_init.add_argument("task_id")
    p_init.add_argument("--objective", required=True)
    p_init.add_argument("--scope", action="append")
    p_init.add_argument("--non-goal", action="append")
    p_init.add_argument("--constraint", action="append")
    p_init.add_argument("--accept", action="append", required=True)
    p_init.add_argument("--stop-condition", action="append")
    p_init.set_defaults(func=cmd_init)

    p_checkpoint = sub.add_parser("checkpoint", help="Persist current progress and next action")
    p_checkpoint.add_argument("task_id")
    p_checkpoint.add_argument("--stage", required=True)
    p_checkpoint.add_argument("--completed", action="append")
    p_checkpoint.add_argument("--next-action", required=True)
    p_checkpoint.set_defaults(func=cmd_checkpoint)

    p_evidence = sub.add_parser("evidence", help="Append an evidence record")
    p_evidence.add_argument("task_id")
    p_evidence.add_argument("--kind", required=True, choices=["test", "command", "diff", "artifact", "review", "manual"])
    p_evidence.add_argument("--summary", required=True)
    p_evidence.add_argument("--command")
    p_evidence.add_argument("--result")
    p_evidence.add_argument("--artifact", action="append")
    p_evidence.set_defaults(func=cmd_evidence)

    p_verify = sub.add_parser("verify", help="Check that durable completion evidence exists")
    p_verify.add_argument("task_id")
    p_verify.set_defaults(func=cmd_verify)

    p_status = sub.add_parser("status", help="Print durable task state")
    p_status.add_argument("task_id")
    p_status.set_defaults(func=cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
