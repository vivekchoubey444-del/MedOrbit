from pathlib import Path
from html import escape
import re

ROOT = Path.cwd()

def write_missing(relative, content):
    path = ROOT / relative
    if path.exists():
        print("KEEP  ", relative)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("CREATE", relative)

def title_from_path(relative):
    name = Path(relative).stem.replace("-", " ").replace("_", " ")
    return " ".join(word.capitalize() for word in name.split())

def page_template(title, relative):
    title_html = escape(title)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#162d4d">
  <meta name="description" content="{title_html} | MEDORBIT education and career guidance.">
  <title>{title_html} | MEDORBIT</title>
  <link rel="stylesheet" href="/assets/css/style.css">
  <script src="/assets/js/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="brand" href="/">MEDORBIT</a>
    <button class="menu-toggle" type="button" aria-expanded="false"
            aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="site-nav" aria-label="Main navigation">
      <a href="/">Home</a>
      <a href="/education/index.html">Education</a>
      <a href="/career/index.html">Careers</a>
      <a href="/pages/study-abroad.html">Study Abroad</a>
      <a href="/pages/about.html">About</a>
      <a href="/pages/contact.html">Contact</a>
    </nav>
  </header>

  <main id="main" class="page-shell">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">/</span>
      <span>{title_html}</span>
    </nav>
    <section class="hero-panel">
      <p class="eyebrow">MEDORBIT • Education and Career Guidance</p>
      <h1>{title_html}</h1>
      <p>Explore course information, admission guidance, eligibility,
         important documents, and your next steps.</p>
    </section>

    <section class="content-panel">
      <h2>Explore your options</h2>
      <p>This page is ready for its dedicated MEDORBIT content. Add
         verified course details, eligibility requirements, fees,
         deadlines, and official links before publishing.</p>
      <div class="card-grid">
        <article class="info-card">
          <h3>Eligibility</h3>
          <p>Review the applicable entry requirements and official criteria.</p>
        </article>
        <article class="info-card">
          <h3>Admission process</h3>
          <p>Check the steps, deadlines, and required documents.</p>
        </article>
        <article class="info-card">
          <h3>Get guidance</h3>
          <p>Contact MEDORBIT for help understanding your available options.</p>
          <a class="text-link" href="/pages/contact.html">Contact us</a>
        </article>
      </div>
    </section>

    <section class="content-panel">
      <h2>Find information</h2>
      <form class="site-search" data-medorbit-search
            data-search-endpoint="/api/v1/search">
        <label for="page-search">Search MEDORBIT</label>
        <div class="search-row">
          <input id="page-search" type="search" name="q"
                 placeholder="Try MBBS, BDS, or careers" required>
          <button type="submit">Search</button>
        </div>
      </form>
      <div data-search-results aria-live="polite"></div>
    </section>
  </main>

  <footer class="site-footer">
    <div>
      <a class="brand" href="/">MEDORBIT</a>
      <p>Education, admissions, and career guidance.</p>
    </div>
    <div class="footer-links">
      <a href="/pages/about.html">About</a>
      <a href="/pages/contact.html">Contact</a>
      <a href="/pages/privacy-policy.html">Privacy</a>
      <a href="/pages/terms.html">Terms</a>
      <a href="/sitemap.html">Sitemap</a>
    </div>
    <p>© <span data-current-year></span> MEDORBIT. Information should be
       verified against the relevant official source.</p>
  </footer>
</body>
</html>
'''

# Required pages: create missing files only.
pages = {
    "education/index.html": "Education and Courses",
    "education/mbbs.html": "MBBS Admissions",
    "education/bds.html": "BDS Admissions",
    "education/bams.html": "BAMS Admissions",
    "education/bums.html": "BUMS Admissions",
    "education/paramedical.html": "Paramedical Courses",
    "education/nursing.html": "Nursing Courses",
    "education/pharmacy.html": "Pharmacy Courses",
    "education/engineering.html": "Engineering Courses",
    "education/management.html": "Management Courses",
    "education/study-material.html": "Study Materials",
    "education/colleges.html": "Colleges and Universities",
    "education/scholarships.html": "Scholarships",
    "education/admission-process.html": "Admission Process",
    "education/entrance-exams.html": "Entrance Examinations",
    "career/index.html": "Career Guidance",
    "career/jobs.html": "Jobs and Opportunities",
    "career/career-options.html": "Career Options",
    "career/recruitment.html": "Recruitment Services",
    "career/job-assistance.html": "Job Assistance",
    "pages/about.html": "About MEDORBIT",
    "pages/contact.html": "Contact MEDORBIT",
    "pages/study-abroad.html": "Study Abroad",
    "pages/faq.html": "Frequently Asked Questions",
    "pages/help-centre.html": "Help Centre",
    "pages/request-guidance.html": "Request Guidance",
    "pages/privacy-policy.html": "Privacy Policy",
    "pages/terms.html": "Terms and Conditions",
    "pages/disclaimer.html": "Disclaimer",
    "pages/accessibility.html": "Accessibility",
    "pages/cookies.html": "Cookie Policy",
    "pages/brochures.html": "Brochures and Guides",
    "pages/notifications.html": "Notifications",
    "404.html": "Page Not Found",
}

for relative, title in pages.items():
    write_missing(relative, page_template(title, relative))

# Shared design system.
write_missing("assets/css/style.css", r'''
:root {
  color-scheme: light;
  --navy: #162d4d;
  --navy-deep: #0d1c32;
  --gold: #d6b66c;
  --cream: #fff8eb;
  --sand: #f2e8d6;
  --ink: #243449;
  --muted: #64748b;
  --line: #d8d2c5;
  --radius: 18px;
  --shadow: 0 12px 32px rgba(13, 28, 50, .09);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
  line-height: 1.65;
  color: var(--ink);
  background: linear-gradient(145deg, #edf1f8, #f8f0e3 65%, #e6edf3);
}
a { color: inherit; }
button, input { font: inherit; }
button, .button {
  display: inline-block;
  border: 1px solid var(--gold);
  border-radius: 10px;
  padding: .7rem 1rem;
  color: var(--navy-deep);
  background: var(--gold);
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
}
button:focus-visible, a:focus-visible, input:focus-visible {
  outline: 3px solid #2c6da5;
  outline-offset: 3px;
}
.skip-link {
  position: absolute; left: -9999px; top: 0;
  background: var(--cream); padding: .7rem; z-index: 100;
}
.skip-link:focus { left: 1rem; }
.site-header {
  position: sticky; top: 0; z-index: 50;
  display: flex; align-items: center; justify-content: space-between;
  gap: 1rem; padding: .85rem clamp(1rem, 4vw, 3rem);
  color: var(--cream); background: var(--navy-deep);
  border-bottom: 2px solid var(--gold);
}
.brand { font-size: 1.2rem; font-weight: 900; letter-spacing: .12em;
  color: var(--gold); text-decoration: none; }
.site-nav { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.site-nav a, .footer-links a { text-decoration: none; }
.site-nav a:hover, .footer-links a:hover { color: var(--gold); }
.menu-toggle { display: none; }
.page-shell { width: min(1160px, 100% - 2rem); margin: 2rem auto; }
.breadcrumbs { color: var(--muted); font-size: .9rem; margin-bottom: 1rem; }
.hero-panel, .content-panel {
  padding: clamp(1.3rem, 4vw, 2.6rem);
  margin-bottom: 1.4rem;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255, 248, 235, .92);
  box-shadow: var(--shadow);
}
.hero-panel { border-top: 4px solid var(--gold); }
.eyebrow { color: #806221; font-size: .8rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
h1, h2, h3 { line-height: 1.2; color: var(--navy); }
h1 { font-size: clamp(2rem, 5vw, 3.5rem); margin: .4rem 0 1rem; }
h2 { font-size: clamp(1.4rem, 3vw, 2rem); }
.card-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
.info-card { padding: 1.2rem; border: 1px solid var(--line); border-radius: 14px; background: #f8f0e3; min-width: 0; }
.text-link { color: #164e8a; font-weight: 700; }
.site-search { margin: 1rem 0; }
.site-search label { display: block; margin-bottom: .5rem; font-weight: 700; }
.search-row { display: flex; gap: .6rem; }
.search-row input { min-width: 0; flex: 1; padding: .75rem; border: 1px solid #a8b2c1; border-radius: 10px; background: #fffaf1; }
[data-search-results] { overflow-wrap: anywhere; }
[data-search-results] li { margin: .5rem 0; }
.site-footer { padding: 2rem clamp(1rem, 4vw, 3rem); color: var(--cream); background: var(--navy-deep); border-top: 3px solid var(--gold); }
.site-footer p { max-width: 75ch; }
.footer-links { display: flex; flex-wrap: wrap; gap: 1rem; margin: 1rem 0; }
@media (max-width: 760px) {
  .site-header { flex-wrap: wrap; }
  .menu-toggle { display: inline-block; }
  .site-nav { display: none; width: 100%; flex-direction: column; align-items: flex-start; padding: .5rem 0; }
  .site-nav.is-open { display: flex; }
  .card-grid { grid-template-columns: 1fr; }
  .search-row { flex-direction: column; }
  .search-row input, .search-row button { width: 100%; }
}
'''.strip() + "\n")

# Shared navigation and progressive enhancements.
write_missing("assets/js/site.js", r'''
(() => {
  "use strict";
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll("[data-current-year]").forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });
})();
'''.strip() + "\n")

# Reusable API-backed search, created only if absent.
write_missing("assets/js/site-search.js", r'''
(() => {
  "use strict";
  document.querySelectorAll("[data-medorbit-search]").forEach((form) => {
    const input = form.querySelector('[name="q"]');
    const output = document.querySelector("[data-search-results]");
    if (!input || !output) return;

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const query = input.value.trim();
      output.replaceChildren();

      if (!query) {
        output.textContent = "Enter a search term.";
        return;
      }

      output.textContent = "Searching…";
      try {
        const endpoint = form.dataset.searchEndpoint || "/api/v1/search";
        const url = new URL(endpoint, window.location.origin);
        url.searchParams.set("q", query);

        const response = await fetch(url, {
          headers: { Accept: "application/json" }
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        output.replaceChildren();

        if (!Array.isArray(data.results) || !data.results.length) {
          output.textContent = "No matching results found.";
          return;
        }

        const list = document.createElement("ul");
        for (const result of data.results) {
          if (typeof result.title !== "string" ||
              typeof result.url !== "string") continue;

          const item = document.createElement("li");
          const link = document.createElement("a");
          link.textContent = result.title;
          link.href = result.url;
          item.appendChild(link);
          list.appendChild(item);
        }

        if (list.children.length) output.appendChild(list);
        else output.textContent = "No valid results returned.";
      } catch (error) {
        console.error("MEDORBIT search failed:", error);
        output.textContent = "Search is unavailable. Please try again later.";
      }
    });
  });
})();
'''.strip() + "\n")

# Ensure the homepage references shared assets without deleting its existing design.
index = ROOT / "index.html"
if index.exists():
    html = index.read_text(encoding="utf-8")
    if "/assets/css/style.css" not in html:
        tag = '<link rel="stylesheet" href="/assets/css/style.css">\n'
        if re.search(r"</head\s*>", html, re.I):
            html = re.sub(r"</head\s*>", tag + "</head>", html, count=1, flags=re.I)
    if "/assets/js/site.js" not in html:
        tag = '<script src="/assets/js/site.js" defer></script>\n'
        if re.search(r"</body\s*>", html, re.I):
            html = re.sub(r"</body\s*>", tag + "</body>", html, count=1, flags=re.I)
        else:
            html += "\n" + tag
    index.write_text(html, encoding="utf-8")
    print("CONNECT index.html")
else:
    write_missing("index.html", page_template("Education and Career Guidance", "index.html"))

# Discover existing HTML files for sitemap and page inventory.
html_files = sorted(
    p for p in ROOT.rglob("*.html")
    if not any(part in {".git", "node_modules", "dist", "coverage"} for part in p.parts)
)

links = "\n".join(
    f'<li><a href="/{escape(p.relative_to(ROOT).as_posix())}">'
    f'{escape(title_from_path(p.relative_to(ROOT).as_posix()))}</a></li>'
    for p in html_files if p.name != "404.html"
)

sitemap_page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sitemap | MEDORBIT</title>
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/site.js" defer></script>
</head><body>
<header class="site-header"><a class="brand" href="/">MEDORBIT</a></header>
<main id="main" class="page-shell"><section class="content-panel">
<h1>MEDORBIT Sitemap</h1><p>Browse available pages.</p><ul>{links}</ul>
</section></main>
<footer class="site-footer">© MEDORBIT</footer>
</body></html>'''

(ROOT / "sitemap.html").write_text(sitemap_page, encoding="utf-8")
print("GENERATE sitemap.html")

# Static-hosting friendly metadata.
write_missing("robots.txt", "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n")
xml_urls = "\n".join(
    f"  <url><loc>/{escape(p.relative_to(ROOT).as_posix())}</loc></url>"
    for p in html_files if p.name != "404.html"
)
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + xml_urls + "\n</urlset>\n",
    encoding="utf-8"
)
print("GENERATE sitemap.xml")

print(f"\nHTML pages found after build: {len(list(ROOT.rglob('*.html')))}")
print("NOTE: New pages are starter templates; add verified content before publishing.")
