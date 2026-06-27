import json
from pathlib import Path

from ticket_triage.schema import TicketClassification

INSTRUCTION = "Classify this support ticket by category and priority."


def format_example(text: str, category: str, priority: str) -> str:
    """Render one labelled row into the training prompt format."""
    label = TicketClassification(category=category, priority=priority)
    completion = json.dumps(
        {"category": label.category.value, "priority": label.priority.value}
    )
    return (
        f"<instruction> {INSTRUCTION}\n"
        f"Ticket: {text}\n"
        f"<response> {completion}"
    )


def format_prompt(text: str) -> str:
    """Render an unlabelled ticket for inference (everything up to <response>)."""
    return (
        f"<instruction> {INSTRUCTION}\n"
        f"Ticket: {text}\n"
        f"<response> "
    )


def load_dataset(path: Path) -> list[dict]:
    """Load and schema-validate a dataset file. Returns rows with a 'formatted' field."""
    rows = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for row in rows:
        TicketClassification(category=row["category"], priority=row["priority"])
        out.append(
            {
                "text": row["text"],
                "category": row["category"],
                "priority": row["priority"],
                "formatted": format_example(row["text"], row["category"], row["priority"]),
            }
        )
    return out