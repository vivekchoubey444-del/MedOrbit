#!/usr/bin/env python3
"""Lightweight SQL migration sanity checks; not a SQL parser."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
migrations = sorted((root / "database" / "migrations").glob("*.sql"))
if not migrations:
    print("ERROR: no SQL migrations found")
    raise SystemExit(1)
errors = []
for file in migrations:
    sql = file.read_text(encoding="utf-8")
    upper = sql.upper()
    if "BEGIN;" not in upper or "COMMIT;" not in upper:
        errors.append(f"{file.name}: expected explicit BEGIN and COMMIT")
    if "DROP DATABASE" in upper:
        errors.append(f"{file.name}: destructive DROP DATABASE statement detected")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"SQL migration files checked: {len(migrations)}")
