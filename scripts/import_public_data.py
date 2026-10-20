import argparse
import hashlib
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "public"
MANIFEST = OUT / "manifest.json"
ALLOWED_HOSTS = {
    "data.gov.in",
    "www.data.gov.in",
    "ap.data.gov.in",
    "aishe.gov.in",
    "www.aishe.gov.in",
    "scholarships.gov.in",
    "www.scholarships.gov.in",
}

parser = argparse.ArgumentParser(
    description="Import a publicly downloadable dataset from an approved source."
)
parser.add_argument("--url", required=True, help="Direct public dataset download URL")
parser.add_argument("--name", required=True, help="Output name, without extension")
args = parser.parse_args()

url = args.url.strip()
name = re.sub(r"[^a-zA-Z0-9_-]", "-", args.name).strip("-")
if not name:
    raise SystemExit("Invalid output name.")

parsed = urlparse(url)
if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
    raise SystemExit(
        "Use an HTTPS direct-download URL from an approved official host. "
        "Do not use login pages, private endpoints, or API keys in URLs."
    )

OUT.mkdir(parents=True, exist_ok=True)
target = OUT / f"{name}.download"
if target.exists():
    raise SystemExit(f"{target} already exists; refusing to overwrite it.")

request = urllib.request.Request(
    url,
    headers={"User-Agent": "MedOrbit-PublicDataImporter/1.0"}
)
try:
    with urllib.request.urlopen(request, timeout=45) as response:
        final_host = urlparse(response.geturl()).hostname
        if final_host not in ALLOWED_HOSTS:
            raise SystemExit(f"Download redirected to unapproved host: {final_host}")
        content_type = response.headers.get("Content-Type", "")
        body = response.read(25 * 1024 * 1024 + 1)
except Exception as exc:
    raise SystemExit(f"Download failed: {exc}")

if len(body) > 25 * 1024 * 1024:
    raise SystemExit("File exceeds 25 MB safety limit; download manually and review it.")
if not body:
    raise SystemExit("Downloaded file is empty.")
if "text/html" in content_type.lower() or body.lstrip().lower().startswith(
    (b"<!doctype html", b"<html")
):
    raise SystemExit(
        "The URL returned an HTML page, not a dataset. Find the direct CSV, JSON, "
        "XML, or ZIP download link on the official source."
    )

suffix = ".json" if "json" in content_type.lower() or body.lstrip().startswith((b"{", b"[")) else (
    ".csv" if "csv" in content_type.lower() else ".bin"
)
if suffix == ".json":
    try:
        json.loads(body.decode("utf-8-sig"))
    except Exception:
        raise SystemExit("Response looks like JSON but failed JSON validation.")

destination = OUT / f"{name}{suffix}"
if destination.exists():
    raise SystemExit(f"{destination} already exists; refusing to overwrite it.")
destination.write_bytes(body)

manifest = []
if MANIFEST.exists():
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        raise SystemExit("Manifest is invalid; fix it before importing more data.")

manifest.append({
    "name": name,
    "file": str(destination.relative_to(ROOT)),
    "source_url": url,
    "retrieved_at": datetime.now(timezone.utc).isoformat(),
    "sha256": hashlib.sha256(body).hexdigest(),
    "content_type": content_type,
    "bytes": len(body),
    "verified": False,
    "note": "Public download; validate schema, license, freshness, and accuracy before production use."
})
MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(f"Saved: {destination.relative_to(ROOT)}")
print(f"Source manifest: {MANIFEST.relative_to(ROOT)}")
print("Downloaded data is not yet integrated into live MedOrbit JSON.")
