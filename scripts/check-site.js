const fs = require("node:fs");
const path = require("node:path");

const root = process.cwd();
const ignored = new Set([
  "node_modules",
  ".git",
  ".next",
  "dist",
  "coverage"
]);

const htmlFiles = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;

    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      walk(fullPath);
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      htmlFiles.push(fullPath);
    }
  }
}

walk(root);

if (htmlFiles.length === 0) {
  console.error("FAIL: No HTML pages found.");
  process.exit(1);
}

let failures = 0;

for (const file of htmlFiles) {
  const html = fs.readFileSync(file, "utf8");
  const relative = path.relative(root, file);

  if (!/<html\b/i.test(html)) {
    console.error(`FAIL: Missing <html> element: ${relative}`);
    failures++;
  }

  if (!/<title\b/i.test(html)) {
    console.error(`WARN: Missing <title>: ${relative}`);
  }

  if (!/<meta\b[^>]*charset/i.test(html)) {
    console.error(`WARN: Missing charset declaration: ${relative}`);
  }
}

console.log(`HTML pages checked: ${htmlFiles.length}`);

if (failures > 0) {
  console.error(`Failed checks: ${failures}`);
  process.exit(1);
}

console.log("PASS: Basic HTML structure checks completed.");
