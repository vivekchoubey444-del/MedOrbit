from pathlib import Path
import re

root = Path(".")
skip = {".git", "node_modules", ".venv", "dist", "build", "coverage"}
changed = 0
for file in root.rglob("*.html"):
    if any(part in skip for part in file.parts):
        continue
    try:
        source = file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    original = source
    if not re.search(r'<link\b[^>]*royal-sapphire\.css', source, re.I):
        tag = '<link rel="stylesheet" href="/assets/css/royal-sapphire.css">'
        if re.search(r'</head\s*>', source, re.I):
            source = re.sub(r'</head\s*>', tag + '\n</head>', source, count=1, flags=re.I)
        else:
            source = tag + '\n' + source
    if not re.search(r'<script\b[^>]*medorbits-global\.js', source, re.I):
        tag = '<script src="/assets/js/medorbits-global.js" defer></script>'
        if re.search(r'</head\s*>', source, re.I):
            source = re.sub(r'</head\s*>', tag + '\n</head>', source, count=1, flags=re.I)
        elif re.search(r'</body\s*>', source, re.I):
            source = re.sub(r'</body\s*>', tag + '\n</body>', source, count=1, flags=re.I)
        else:
            source += '\n' + tag
    if source != original:
        file.write_text(source, encoding="utf-8")
        changed += 1

print(f"Added shared theme references to {changed} HTML file(s).")
