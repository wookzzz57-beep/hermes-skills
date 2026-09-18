from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter")
    data: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> int:
    failures: list[str] = []
    files = sorted(SKILLS.glob("*/SKILL.md"))
    if not files:
        failures.append("no skills found")
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
            meta = parse_frontmatter(text)
            name = meta.get("name", "")
            desc = meta.get("description", "")
            if not NAME_RE.fullmatch(name):
                failures.append(f"{path}: invalid name")
            if not desc:
                failures.append(f"{path}: missing description")
            if "TODO" in text:
                failures.append(f"{path}: contains TODO")
        except Exception as exc:
            failures.append(f"{path}: {exc}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"validated {len(files)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
