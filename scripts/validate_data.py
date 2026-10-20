#!/usr/bin/env python3
"""Validate MedOrbit JSON data files without changing them."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "assets" / "data"
errors = []
count = 0

for file in sorted(DATA.glob("*.json")):
    count += 1
    try:
        value = json.loads(file.read_text(encoding="utf-8"))
        if not isinstance(value, (dict, list)):
            errors.append(f"{file.relative_to(ROOT)}: top-level value must be an object or array")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{file.relative_to(ROOT)}: {exc}")

print(f"JSON files checked: {count}")
if errors:
    print("\n".join("ERROR: " + e for e in errors))
    raise SystemExit(1)
print("All JSON data files are valid.")
