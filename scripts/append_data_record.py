import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="JSON file relative to repository root")
parser.add_argument("--record", required=True, help="JSON object to append")
args = parser.parse_args()

target = (ROOT / args.file).resolve()
if ROOT.resolve() not in target.parents:
    raise SystemExit("Target must be inside the repository.")
if target.suffix.lower() != ".json":
    raise SystemExit("Target must be a JSON file.")

record = json.loads(args.record)
if not isinstance(record, dict) or not record.get("id"):
    raise SystemExit("Record must be a JSON object with a unique id.")

existing = json.loads(target.read_text(encoding="utf-8")) if target.exists() else []
if not isinstance(existing, list):
    raise SystemExit("Target JSON must contain an array.")
if any(isinstance(item, dict) and item.get("id") == record["id"] for item in existing):
    raise SystemExit("Duplicate id; no changes made.")

existing.append(record)
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Appended {record['id']} to {target.relative_to(ROOT)}")
