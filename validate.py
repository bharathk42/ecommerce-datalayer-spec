"""Validate captured dataLayer pushes against datalayer.schema.json.

Usage: python validate.py events.json
events.json is a JSON array of dataLayer push objects.
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).with_name("datalayer.schema.json")


def main(path: str) -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema)
    events = json.loads(Path(path).read_text())

    failed = 0
    for i, event in enumerate(events):
        name = event.get("event", "<no event>")
        errors = sorted(validator.iter_errors(event), key=lambda e: list(e.path))
        if errors:
            failed += 1
            err = errors[0]
            where = ".".join(str(p) for p in err.path) or "<root>"
            print(f"[FAIL] #{i} {name} -> {where}: {err.message}")
        else:
            print(f"[PASS] #{i} {name}")

    print(f"{len(events) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
