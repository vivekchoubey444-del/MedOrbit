const fs = require("node:fs");
const path = require("node:path");

const root = process.cwd();
const ignored = new Set([
  ".git", "node_modules", ".next", "dist", "coverage"
]);
const htmlFiles = [];
const issues = [];
const checked = new Set();

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;

    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.isFile() && entry.name.endsWith(".html")) {
      htmlFiles.push(full);
    }
  }
}

function checkReference(value, source) {
  value = value.trim().replaceAll("&amp;", "&");

  if (!value || /^(#|https?:|mailto:|tel:|javascript:|data:|blob:)/i.test(value)) return;
  if (value.startsWith("//")) return;

  const clean = value.split("#")[0].split("?")[0];
  if (!clean) return;

  let target;

  if (clean.startsWith("/")) {
    target = path.join(root, clean.replace(/^\/+/, ""));
  } else {
    target = path.resolve(path.dirname(source), decodeURIComponent(clean));
  }

  if (checked.has(target)) return;
  checked.add(target);

  if (!fs.existsSync(target)) {
    issues.push(`${path.relative(root, source)} -> missing: ${value}`);
  }
}

walk(root);

for (const file of htmlFiles) {
  const html = fs.readFileSync(file, "utf8");

  const patterns = [
    /\b(?:href|src|poster|data-src)\s*=\s*["']([^"']+)["']/gi
  ];

  for (const pattern of patterns) {
    for (const match of html.matchAll(pattern)) {
      checkReference(match[1], file);
    }
  }
}

console.log(`HTML pages scanned: ${htmlFiles.length}`);
console.log(`Local references checked: ${checked.size}`);

if (issues.length) {
  console.log(`\nMissing references (${issues.length}):`);
  for (const issue of issues) console.log(`- ${issue}`);
  process.exitCode = 1;
} else {
  console.log("PASS: All scanned local references exist.");
}
