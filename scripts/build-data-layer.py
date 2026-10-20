from pathlib import Path
import json
import re
from datetime import date

ROOT = Path.cwd()
DATA = ROOT / "assets" / "data"
JS = ROOT / "assets" / "js"
DATA.mkdir(parents=True, exist_ok=True)
JS.mkdir(parents=True, exist_ok=True)

def save_if_missing(path, content):
    if path.exists():
        print("KEEP existing:", path.relative_to(ROOT))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("CREATE:", path.relative_to(ROOT))

def save_json_if_missing(name, description, fields):
    path = DATA / name
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"WARNING: Existing {name} is invalid JSON: {exc}")
        else:
            print("KEEP existing dataset:", name)
        return

    document = {
        "schemaVersion": 1,
        "dataset": path.stem,
        "description": description,
        "updatedAt": date.today().isoformat(),
        "sourcePolicy": (
            "Verify factual, legal, admission, fee and deadline information "
            "against official sources before publication."
        ),
        "items": [],
        "fields": fields
    }
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print("CREATE dataset:", name)

datasets = {
    "courses.json": (
        "Courses and course categories",
        ["id", "title", "category", "description", "eligibility", "duration", "officialUrl"]
    ),
    "colleges.json": (
        "College directory",
        ["id", "name", "state", "city", "courseIds", "officialUrl", "source", "verifiedAt"]
    ),
    "universities.json": (
        "University directory",
        ["id", "name", "country", "city", "officialUrl", "source", "verifiedAt"]
    ),
    "scholarships.json": (
        "Scholarships and funding opportunities",
        ["id", "title", "provider", "eligibility", "deadline", "officialUrl", "verifiedAt"]
    ),
    "hostels.json": (
        "Hostel and accommodation directory",
        ["id", "name", "collegeId", "location", "officialUrl", "verifiedAt"]
    ),
    "fees.json": (
        "Course and institution fee information",
        ["id", "collegeId", "courseId", "academicYear", "tuitionFee", "currency", "source", "verifiedAt"]
    ),
    "admission-process.json": (
        "Admission process and steps",
        ["id", "courseId", "step", "title", "description", "officialUrl"]
    ),
    "entrance-exams.json": (
        "Entrance examination information",
        ["id", "name", "courses", "organizer", "officialUrl", "verifiedAt"]
    ),
    "documents.json": (
        "Document checklists",
        ["id", "courseId", "documentName", "required", "notes", "officialSource"]
    ),
    "career-options.json": (
        "Career pathways",
        ["id", "title", "field", "description", "qualifications", "relatedCourseIds"]
    ),
    "jobs.json": (
        "Job listings",
        ["id", "title", "employer", "location", "employmentType", "officialUrl", "publishedAt", "expiresAt"]
    ),
    "faqs.json": (
        "Frequently asked questions",
        ["id", "question", "answer", "category", "source"]
    ),
    "news.json": (
        "News and announcements",
        ["id", "title", "summary", "publishedAt", "officialUrl", "source"]
    ),
    "notifications.json": (
        "Public site notifications",
        ["id", "title", "message", "severity", "publishedAt", "expiresAt"]
    ),
    "testimonials.json": (
        "Approved testimonials",
        ["id", "displayName", "content", "course", "consentVerified"]
    ),
    "services.json": (
        "MEDORBIT service catalogue",
        ["id", "title", "description", "category", "contactUrl"]
    ),
    "pages.json": (
        "Page directory and metadata",
        ["id", "title", "url", "category", "description"]
    ),
    "navigation.json": (
        "Shared navigation structure",
        ["label", "url", "children"]
    ),
    "site-config.json": (
        "Public site configuration; never put secrets here",
        ["siteName", "defaultLanguage", "supportUrl", "searchEndpoint"]
    )
}

for filename, (description, fields) in datasets.items():
    save_json_if_missing(filename, description, fields)

# Initial public navigation and configuration data.
initial_data = {
    "navigation.json": {
        "schemaVersion": 1,
        "items": [
            {"label": "Home", "url": "/"},
            {"label": "Education", "url": "/education/index.html"},
            {"label": "Careers", "url": "/career/index.html"},
            {"label": "Study Abroad", "url": "/pages/study-abroad.html"},
            {"label": "About", "url": "/pages/about.html"},
            {"label": "Contact", "url": "/support/contact.html"}
        ]
    },
    "site-config.json": {
        "schemaVersion": 1,
        "siteName": "MEDORBIT",
        "defaultLanguage": "en",
        "searchEndpoint": "/api/v1/search",
        "supportUrl": "/support/contact.html"
    }
}

for name, obj in initial_data.items():
    path = DATA / name
    if not path.exists():
        path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
        print("CREATE starter data:", name)

# Shared browser-side data service.
save_if_missing(JS / "data-service.js", r'''
(() => {
  "use strict";

  const cache = new Map();

  async function load(name) {
    if (!/^[a-z0-9-]+$/.test(name)) {
      throw new Error("Invalid dataset name");
    }

    if (cache.has(name)) return cache.get(name);

    const request = fetch(`/assets/data/${name}.json`, {
      headers: { Accept: "application/json" }
    }).then(async (response) => {
      if (!response.ok) {
        throw new Error(`Dataset ${name} returned HTTP ${response.status}`);
      }
      return response.json();
    });

    cache.set(name, request);

    try {
      return await request;
    } catch (error) {
      cache.delete(name);
      throw error;
    }
  }

  function renderList(container, items, fields) {
    container.replaceChildren();

    if (!Array.isArray(items) || items.length === 0) {
      container.textContent = "Information will be published after verification.";
      return;
    }

    const list = document.createElement("ul");

    for (const item of items) {
      const li = document.createElement("li");
      const title = item.title || item.name || item.question || item.label || "Item";
      const heading = document.createElement("strong");
      heading.textContent = String(title);
      li.appendChild(heading);

      for (const field of fields) {
        if (field === "title" || field === "name") continue;
        const value = item[field];
        if (value === undefined || value === null || value === "") continue;
        const p = document.createElement("p");
        p.textContent = `${field}: ${String(value)}`;
        li.appendChild(p);
      }

      list.appendChild(li);
    }

    container.appendChild(list);
  }

  async function connect(root = document) {
    const elements = root.querySelectorAll("[data-data-source]");

    for (const element of elements) {
      const dataset = element.dataset.dataSource;
      const fields = (element.dataset.fields || "description")
        .split(",").map((field) => field.trim()).filter(Boolean);

      try {
        const data = await load(dataset);
        renderList(element, data.items, fields);
      } catch (error) {
        console.error("MEDORBIT data connection failed:", error);
        element.textContent = "Information is temporarily unavailable.";
      }
    }
  }

  window.MEDORBIT_DATA = Object.freeze({ load, connect });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => connect());
  } else {
    connect();
  }
})();
'''.strip() + "\n")

# Build inventory and page-to-JS mapping from actual files.
ignored = {".git", "node_modules", ".next", "dist", "coverage", ".venv", "venv"}

html_files = sorted(
    p for p in ROOT.rglob("*.html")
    if not any(part in ignored for part in p.relative_to(ROOT).parts)
)
js_files = sorted(
    p for p in ROOT.rglob("*.js")
    if not any(part in ignored for part in p.relative_to(ROOT).parts)
)

page_records = []
for path in html_files:
    rel = "/" + path.relative_to(ROOT).as_posix()
    html = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    title = re.sub(r"\s+", " ", match.group(1)).strip() if match else path.stem.replace("-", " ").title()

    scripts = re.findall(
        r'<script\b[^>]*\bsrc=["\']([^"\']+)["\']',
        html, re.I
    )
    page_records.append({
        "id": path.relative_to(ROOT).as_posix(),
        "title": title,
        "url": "/" if path.name == "index.html" and path.parent == ROOT else rel,
        "category": path.parent.relative_to(ROOT).as_posix(),
        "description": "Generated from the current HTML page inventory.",
        "scriptReferences": scripts
    })

inventory = {
    "schemaVersion": 1,
    "generatedFrom": "Current repository files",
    "pages": page_records,
    "javascriptFiles": [
        "/" + p.relative_to(ROOT).as_posix() for p in js_files
    ]
}
(DATA / "project-inventory.json").write_text(
    json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)

# Add the shared service to HTML files only when it is not already included.
for path in html_files:
    html = path.read_text(encoding="utf-8", errors="replace")
    if "/assets/js/data-service.js" in html:
        continue

    tag = '<script src="/assets/js/data-service.js" defer></script>\n'
    if re.search(r"</body\s*>", html, re.I):
        html = re.sub(r"</body\s*>", tag + "</body>", html, count=1, flags=re.I)
        path.write_text(html, encoding="utf-8")
        print("CONNECTED data service:", path.relative_to(ROOT))

print(f"\nHTML pages inventoried: {len(html_files)}")
print(f"JavaScript files inventoried: {len(js_files)}")
print("Generated assets/data/project-inventory.json")
