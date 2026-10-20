from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {".git", "node_modules", ".next"}
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ("href","src") and value:
                self.refs.append((tag,key,value))
pages=[p for p in ROOT.rglob("*.html") if not any(x in EXCLUDE for x in p.parts)]
missing=[]
for page in pages:
    try:
        parser=Parser(); parser.feed(page.read_text(encoding="utf-8"))
    except Exception as exc:
        print("READ ERROR",page,exc); continue
    for tag,key,ref in parser.refs:
        if ref.startswith(("#","http:","https:","//","mailto:","tel:","data:","javascript:")): continue
        path=urlparse(ref).path
        if not path: continue
        target=(ROOT/unquote(path.lstrip("/"))) if path.startswith("/") else (page.parent/unquote(path))
        if not target.exists(): missing.append((page.relative_to(ROOT),ref))
print(f"HTML pages checked: {len(pages)}")
print(f"Missing local references: {len(missing)}")
for page,ref in missing: print(f"  {page} -> {ref}")
