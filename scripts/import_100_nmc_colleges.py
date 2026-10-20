import json, re, hashlib, sys
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from datetime import date

URL = "https://www.nmc.org.in/information-desk/for-students-to-study-in-india/list-of-college-teaching-mbbs/1000/"
SOURCE = "https://www.nmc.org.in/information-desk/for-students-to-study-in-india/list-of-college-teaching-mbbs/1000/"
DEST = Path("data/colleges.json")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows=[]; self.row=None; self.cell=None; self.table=False
    def handle_starttag(self, tag, attrs):
        if tag=="table": self.table=True
        elif self.table and tag=="tr": self.row=[]
        elif self.table and tag in ("td","th"): self.cell=[]
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if self.table and tag in ("td","th") and self.cell is not None:
            self.row.append(re.sub(r"\s+"," ","".join(self.cell)).strip()); self.cell=None
        elif self.table and tag=="tr" and self.row is not None:
            if self.row: self.rows.append(self.row)
            self.row=None
        elif tag=="table": self.table=False

print("1/4 Downloading NMC listing...", flush=True)
try:
    req=Request(URL,headers={"User-Agent":"Mozilla/5.0"})
    with urlopen(req,timeout=25) as response:
        html=response.read(15_000_000).decode("utf-8","replace")
except Exception as e:
    sys.exit(f"DOWNLOAD FAILED: {e}\nNo college records changed.")

Path("data/public").mkdir(parents=True,exist_ok=True)
Path("data/public/nmc-mbbs-listing.html").write_text(html,encoding="utf-8")
print("2/4 Parsing source page...", flush=True)
p=Parser(); p.feed(html)
records=[]
for row in p.rows:
    joined=" | ".join(row)
    if len(row)<4 or not re.search(r"\bMBBS\b",joined,re.I):
        continue
    # The source table layout varies; preserve each row rather than guessing
    # which column contains the seat count or recognition status.
    name=max(row,key=len).strip()
    if len(name)<8 or "college" not in name.lower() and "institute" not in name.lower() and "medical" not in name.lower():
        continue
    state = next((v for v in row if re.search(r"\b(Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chhattisgarh|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|Jammu and Kashmir|Ladakh|Puducherry|Chandigarh)\b",v,re.I)),None)
    ident="IN-NMC-"+hashlib.sha256((state or "") .__add__("|"+name).lower().encode()).hexdigest()[:16].upper()
    records.append({
      "id":ident,"name":name,"country":"India","state":state,
      "course":"MBBS","source":SOURCE,"source_row":row,
      "last_checked":date.today().isoformat(),
      "data_status":"source_row_imported_review_columns_before_use"
    })

if not records:
    sys.exit("No rows were safely recognized. Existing colleges.json was not changed. Inspect data/public/nmc-mbbs-listing.html.")

unique={r["id"]:r for r in records}
incoming=list(unique.values())[:100]
print("3/4 Loading existing college data...",flush=True)
if DEST.exists():
    current=json.loads(DEST.read_text(encoding="utf-8"))
else:
    current=[]
if not isinstance(current,list):
    sys.exit("data/colleges.json must be an array. Existing file was not changed.")
ids={x.get("id") for x in current if isinstance(x,dict)}
names={re.sub(r"\W+","",x.get("name","").lower()) for x in current if isinstance(x,dict)}
added=[]
for r in incoming:
    normalized=re.sub(r"\W+","",r["name"].lower())
    if r["id"] in ids or normalized in names: continue
    added.append(r); ids.add(r["id"]); names.add(normalized)

print("4/4 Saving records...",flush=True)
tmp=DEST.with_suffix(".json.tmp")
tmp.write_text(json.dumps(current+added,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
json.loads(tmp.read_text(encoding="utf-8"))
tmp.replace(DEST)
print(f"Downloaded rows: {len(incoming)}")
print(f"New rows appended: {len(added)}")
print(f"Total records: {len(current)+len(added)}")
print(f"Saved to {DEST}")
print("Review source_row and verify each record before publishing.")
