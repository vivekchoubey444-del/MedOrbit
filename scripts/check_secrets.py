#!/usr/bin/env python3
"""Basic secret-pattern check. Not a replacement for a dedicated secret scanner."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {".git", "node_modules", ".venv", "backups"}
PATTERNS = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("common token assignment", re.compile(r"(?i)\b(?:api_key|access_token|client_secret)\s*[:=]\s*['\"][^'\"]{16,}['\"]")),
]
errors = []
for file in ROOT.rglob("*"):
    if not file.is_file() or any(p in EXCLUDE for p in file.parts):
        continue
    if file.suffix.lower() not in {".js",".json",".py",".yml",".yaml",".html",".sql",".env",".md"}:
        continue
    if file.name in {".env.example"}:
        continue
    try:
        text = file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        continue
    for label, pattern in PATTERNS:
        if pattern.search(text):
            errors.append(f"{file.relative_to(ROOT)}: possible {label}; review manually")

if errors:
    print("\n".join("REVIEW: " + x for x in errors))
    raise SystemExit(1)
print("No matching high-confidence secret patterns found.")
