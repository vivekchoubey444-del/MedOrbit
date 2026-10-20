import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/resources/education-resources.json"
REPORT = ROOT / "reports/official-pdf-download-report.json"

items = json.loads(REGISTRY.read_text(encoding="utf-8"))
report = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "downloads": [],
    "note": "Only selected official PDFs are attempted; this does not mirror all Google results."
}

allowed_hosts = {
    "aicte-qa.aicte-india.org",
    "www.nmc.org.in"
}

for item in items:
    rel = item.get("local_path")
    if not rel:
        continue

    dest = ROOT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = item["source_url"]

    from urllib.parse import urlparse
    host = urlparse(url).hostname
    if host not in allowed_hosts:
        report["downloads"].append({
            "id": item["id"], "status": "blocked_unapproved_host"
        })
        continue

    if dest.exists() and dest.stat().st_size > 1000 and dest.read_bytes()[:5] == b"%PDF-":
        item["status"] = "already_downloaded"
        report["downloads"].append({
            "id": item["id"], "status": "already_downloaded", "path": rel
        })
        continue

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MedOrbit-Education-Resource-Importer/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read(30 * 1024 * 1024 + 1)

        if len(data) > 30 * 1024 * 1024:
            raise ValueError("PDF exceeds 30 MB safety limit")
        if not data.startswith(b"%PDF-"):
            raise ValueError(f"Response is not a PDF (Content-Type: {content_type})")

        temp = dest.with_suffix(dest.suffix + ".tmp")
        temp.write_bytes(data)
        temp.replace(dest)
        item["status"] = "downloaded"
        report["downloads"].append({
            "id": item["id"], "status": "downloaded",
            "path": rel, "bytes": len(data)
        })
        print("DOWNLOADED", rel, len(data), "bytes")
    except Exception as exc:
        item["status"] = "download_failed_or_unavailable"
        report["downloads"].append({
            "id": item["id"], "status": "failed",
            "reason": str(exc)[:300], "source_url": url
        })
        print("SKIPPED", item["id"], str(exc))

REGISTRY.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Download report:", REPORT)
