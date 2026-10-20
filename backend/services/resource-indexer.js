"use strict";

const fs = require("node:fs/promises");
const path = require("node:path");

const DATA = path.resolve(__dirname, "../../assets/data");

async function refreshReleases() {
  await fs.mkdir(DATA, { recursive: true });
  const file = path.join(DATA, "recent-releases.json");
  let current = { items: [] };

  try {
    current = JSON.parse(await fs.readFile(file, "utf8"));
  } catch {}

  const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000;
  const items = (current.items || []).filter(item => {
    const date = Date.parse(item.publishedAt || "");
    return Number.isFinite(date) && date >= cutoff && date <= Date.now();
  });

  const result = {
    schemaVersion: 1,
    windowDays: 7,
    updatedAt: new Date().toISOString(),
    items
  };

  const temp = file + ".tmp";
  await fs.writeFile(temp, JSON.stringify(result, null, 2) + "\n");
  await fs.rename(temp, file);
  return result;
}

module.exports = { refreshReleases };
