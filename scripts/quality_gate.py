import json
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

errors = []
warnings = []
summary = {"json_files": 0, "records_checked": 0, "warnings": [], "errors": []}

def walk_records(value, location):
    if isinstance(value, list):
        for i, item in enumerate(value):
            if isinstance(item, dict):
                yield item, f"{location}[{i}]"
            elif isinstance(item, (list, dict)):
                yield from walk_records(item, f"{location}[{i}]")
    elif isinstance(value, dict):
        for key in ("records", "data", "items", "colleges",
                    "universities", "courses", "jobs", "services"):
            child = value.get(key)
            if isinstance(child, list):
                yield from walk_records(child, f"{location}.{key}")
                return
        if any(k in value for k in ("id", "slug", "name", "title")):
            yield value, location

if DATA.exists():
    for path in sorted(DATA.rglob("*.json")):
        if any(part in {".git", "node_modules"} for part in path.parts):
            continue
        if ".backup" in path.name or ".bak" in path.name:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            summary["json_files"] += 1
        except Exception as exc:
            errors.append(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
            continue

        identities = Counter()
        for record, where in walk_records(payload, str(path.relative_to(ROOT))):
            summary["records_checked"] += 1
            identity = record.get("id") or record.get("slug")
            if identity is not None:
                normalized = str(identity).strip().casefold()
                if normalized:
                    identities[normalized] += 1

        duplicates = [key for key, count in identities.items() if count > 1]
        if duplicates:
            warnings.append(
                f"{path.relative_to(ROOT)} has duplicate IDs/slugs: "
                + ", ".join(duplicates[:10])
            )

if not DATA.exists():
    warnings.append("No data/ directory found.")

summary["warnings"] = warnings
summary["errors"] = errors
report_path = REPORTS / "quality-gate-report.json"
report_path.write_text(
    json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)

print(f"JSON files checked: {summary['json_files']}")
print(f"Records checked: {summary['records_checked']}")
for item in warnings:
    print("WARNING:", item)
for item in errors:
    print("ERROR:", item)
print("Report:", report_path)

if errors:
    sys.exit(1)
print("QUALITY GATE PASSED: JSON is parseable.")
