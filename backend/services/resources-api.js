"use strict";

const fs = require("node:fs/promises");
const path = require("node:path");

const DATA = path.resolve(__dirname, "../../assets/data");

async function readStore(filename) {
  try {
    return JSON.parse(await fs.readFile(path.join(DATA, filename), "utf8"));
  } catch {
    return { items: [] };
  }
}

function sendJson(res, status, body) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  res.end(JSON.stringify(body));
}

async function handleResourcesApi(req, res) {
  const url = new URL(req.url, "http://localhost");
  if (!url.pathname.startsWith("/api/v1/resources/")) return false;

  if (req.method === "GET" &&
      url.pathname === "/api/v1/resources/pdfs") {
    const data = await readStore("pdf-library.json");
    const q = (url.searchParams.get("q") || "").toLowerCase();
    const category = (url.searchParams.get("category") || "").toLowerCase();

    const items = (data.items || []).filter(item => {
      const searchable = [
        item.title, item.description, item.category
      ].filter(Boolean).join(" ").toLowerCase();

      return (!q || searchable.includes(q)) &&
        (!category || String(item.category || "").toLowerCase() === category);
    });

    sendJson(res, 200, { updatedAt: data.updatedAt || null, items });
    return true;
  }

  if (req.method === "GET" &&
      url.pathname === "/api/v1/resources/releases") {
    const data = await readStore("recent-releases.json");
    const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const q = (url.searchParams.get("q") || "").toLowerCase();
    const category = (url.searchParams.get("category") || "").toLowerCase();

    const items = (data.items || []).filter(item => {
      const date = Date.parse(item.publishedAt || "");
      const searchable = [
        item.title, item.description, item.category, item.sourceName
      ].filter(Boolean).join(" ").toLowerCase();

      return Number.isFinite(date) && date >= cutoff && date <= Date.now() &&
        (!q || searchable.includes(q)) &&
        (!category || String(item.category || "").toLowerCase() === category);
    });

    sendJson(res, 200, {
      windowDays: 7,
      updatedAt: data.updatedAt || null,
      items
    });
    return true;
  }

  sendJson(res, 405, { message: "Method not allowed for this resource endpoint." });
  return true;
}

module.exports = { handleResourcesApi };
