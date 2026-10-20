import json, re
from pathlib import Path

ROOT = Path(".")
DATA_DIRS = ["data", "assets/data", "backend/data"]
PLACEHOLDERS = re.compile(
    r"synthetic|placeholder|dummy|sample|example|test data|lorem ipsum|"
    r"replace me|your api|fake data|demo record",
    re.I
)
report = []

for folder in DATA_DIRS:
    base = ROOT / folder
    if not base.exists():
        continue
    for path in base.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            report.append({
                "file": str(path), "status": "INVALID_JSON",
                "details": str(exc)
            })
            continue

        records = data if isinstance(data, list) else (
            next((v for v in data.values() if isinstance(v, list)), None)
            if isinstance(data, dict) else None
        )
        text = json.dumps(data, ensure_ascii=False)
        flags = []
        if PLACEHOLDERS.search(text):
            flags.append("possible synthetic or placeholder values")

        def inspect(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in {"source", "source_url", "sourceurl",
                                       "official_url", "verified_at",
                                       "last_verified"}:
                        continue
                    if key.lower() in {"name", "title", "college", "university",
                                       "employer", "job_title"} and isinstance(value, str):
                        if re.search(r"^(test|sample|demo|example)\b", value, re.I):
                            flags.append(f"placeholder in field: {key}")
                    inspect(value)
            elif isinstance(obj, list):
                for item in obj:
                    inspect(item)
        inspect(data)

        report.append({
            "file": str(path),
            "status": "REVIEW_REQUIRED" if flags else "NO_OBVIOUS_PLACEHOLDER",
            "records": len(records) if isinstance(records, list) else None,
            "flags": sorted(set(flags)),
            "has_source_metadata": any(
                key in text for key in ["source_url", "official_url", "verified_at"]
            )
        })

out = ROOT / "reports"
out.mkdir(exist_ok=True)
destination = out / "real-data-migration-report.json"
destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8")
print(f"Scanned {len(report)} JSON files.")
print(f"Report: {destination}")
print("No source data was changed. Verify records against official sources before importing.")
