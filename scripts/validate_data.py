import json
from collections import Counter
from pathlib import Path

from pydantic import ValidationError

from ticket_triage.schema import TicketClassification


def validate_file(path: Path) -> None:
    if not path.exists():
        print(f"\n{path} not found — skipping")
        return

    rows = json.loads(path.read_text(encoding="utf-8"))
    print(f"\n{path}  ({len(rows)} rows)")

    cat_counts: Counter = Counter()
    prio_counts: Counter = Counter()
    errors = []

    for i, row in enumerate(rows):
        try:
            parsed = TicketClassification(
                category=row["category"],
                priority=row["priority"],
            )
        except (ValidationError, KeyError) as e:
            errors.append((i, e))
            continue
        cat_counts[parsed.category.value] += 1
        prio_counts[parsed.priority.value] += 1

    print("  categories:")
    for cat, n in sorted(cat_counts.items()):
        print(f"    {cat:16} {n}")
    print("  priorities:")
    for prio, n in sorted(prio_counts.items()):
        print(f"    {prio:16} {n}")

    if errors:
        print(f"  {len(errors)} INVALID rows (bad/typo label or missing field):")
        for i, e in errors[:10]:
            print(f"    row {i}: {type(e).__name__}")
    else:
        print("  all rows valid against schema")


if __name__ == "__main__":
    for name in ("train.json", "test.json"):
        validate_file(Path("data") / name)