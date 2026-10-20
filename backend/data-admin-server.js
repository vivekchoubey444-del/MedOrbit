"use strict";
const http = require("node:http");
const fs = require("node:fs/promises");
const path = require("node:path");
const crypto = require("node:crypto");

const ROOT = path.resolve(__dirname, "..");
const PORT = Number(process.env.DATA_ADMIN_PORT || 3030);
const TOKEN = process.env.ADMIN_TOKEN || "";
const GOOGLE_KEY = process.env.GOOGLE_API_KEY || "";
const GOOGLE_CX = process.env.GOOGLE_CX || "";
const TARGETS = {
  colleges: "data/colleges.json",
  universities: "data/universities.json",
  courses: "data/courses.json",
  scholarships: "data/scholarships.json",
  jobs: "data/jobs.json",
  services: "data/services.json"
};
const PUBLIC_RESULTS = "data/public/google-search-results.json";

function send(res, status, value) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  res.end(JSON.stringify(value, null, 2));
}
function authorized(req, body) {
  const supplied = req.headers["x-admin-token"] || body.token || "";
  if (!TOKEN || TOKEN.length < 24) return false;
  const a = Buffer.from(String(supplied));
  const b = Buffer.from(TOKEN);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
async function readBody(req) {
  let raw = "";
  for await (const chunk of req) {
    raw += chunk;
    if (Buffer.byteLength(raw) > 2 * 1024 * 1024)
      throw new Error("Request exceeds 2 MB limit.");
  }
  return raw ? JSON.parse(raw) : {};
}
function localFile(relative) {
  const full = path.resolve(ROOT, relative);
  if (!full.startsWith(ROOT + path.sep)) throw new Error("Invalid file path.");
  return full;
}
async function readArray(relative) {
  const file = localFile(relative);
  try {
    const parsed = JSON.parse(await fs.readFile(file, "utf8"));
    if (!Array.isArray(parsed)) throw new Error(`${relative} must contain a JSON array.`);
    return parsed;
  } catch (err) {
    if (err.code === "ENOENT") return [];
    throw err;
  }
}
async function writeArray(relative, data) {
  const file = localFile(relative);
  await fs.mkdir(path.dirname(file), { recursive: true });
  const temp = file + ".tmp";
  await fs.writeFile(temp, JSON.stringify(data, null, 2) + "\n", { flag: "wx" });
  await fs.rename(temp, file);
}
const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
    if (req.method === "GET" && url.pathname === "/") {
      res.writeHead(200, {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff"
      });
      return res.end(await fs.readFile(path.join(ROOT, "admin/data.html")));
    }
    if (req.method === "GET" && url.pathname === "/api/health")
      return send(res, 200, { ok: true, service: "MedOrbit Data Manager" });

    if (!url.pathname.startsWith("/api/admin/"))
      return send(res, 404, { error: "Not found" });

    const body = ["POST", "PUT"].includes(req.method) ? await readBody(req) : {};
    if (!authorized(req, body))
      return send(res, 401, { error: "Unauthorized. Set a valid ADMIN_TOKEN." });

    if (req.method === "GET" && url.pathname === "/api/admin/files")
      return send(res, 200, { files: Object.keys(TARGETS) });

    if (req.method === "POST" && url.pathname === "/api/admin/import") {
      const relative = TARGETS[body.target];
      if (!relative) return send(res, 400, { error: "Unknown data target." });
      const incoming = Array.isArray(body.records) ? body.records : [body.records];
      if (!incoming.length || incoming.length > 1000 ||
          incoming.some(x => !x || typeof x !== "object" || Array.isArray(x)))
        return send(res, 400, { error: "Provide 1–1000 JSON objects." });

      const current = await readArray(relative);
      const ids = new Set(current.map(x => x && x.id).filter(Boolean));
      for (const item of incoming) {
        if (item.id && ids.has(item.id))
          return send(res, 409, { error: `Duplicate id: ${item.id}. No records were imported.` });
      }
      await writeArray(relative, current.concat(incoming));
      return send(res, 200, {
        ok: true, target: body.target,
        added: incoming.length, total: current.length + incoming.length
      });
    }

    if (req.method === "POST" && url.pathname === "/api/admin/google-search") {
      if (!GOOGLE_KEY || !GOOGLE_CX)
        return send(res, 503, {
          error: "Google search is not configured. Set GOOGLE_API_KEY and GOOGLE_CX."
        });
      const q = String(body.query || "").trim();
      if (!q || q.length > 300) return send(res, 400, { error: "Query must be 1–300 characters." });

      const endpoint = new URL("https://www.googleapis.com/customsearch/v1");
      endpoint.searchParams.set("key", GOOGLE_KEY);
      endpoint.searchParams.set("cx", GOOGLE_CX);
      endpoint.searchParams.set("q", q);
      endpoint.searchParams.set("num", "10");
      const upstream = await fetch(endpoint, { signal: AbortSignal.timeout(15000) });
      const result = await upstream.json();
      if (!upstream.ok)
        return send(res, 502, { error: "Google search request failed.", details: result.error?.message || upstream.statusText });

      const entries = (result.items || []).map(item => ({
        id: crypto.createHash("sha256").update(item.link || item.title || "").digest("hex").slice(0, 20),
        title: item.title || "",
        url: item.link || "",
        snippet: item.snippet || "",
        source: "Google Custom Search",
        query: q,
        retrieved_at: new Date().toISOString(),
        review_status: "pending",
        note: "Search result only; verify facts against the original source before importing."
      }));
      const prior = await readArray(PUBLIC_RESULTS);
      const seen = new Set(prior.map(x => x.url));
      const fresh = entries.filter(x => x.url && !seen.has(x.url));
      await writeArray(PUBLIC_RESULTS, prior.concat(fresh));
      return send(res, 200, { ok: true, found: entries.length, saved: fresh.length, review_file: PUBLIC_RESULTS, results: entries });
    }

    return send(res, 404, { error: "Unknown admin endpoint." });
  } catch (err) {
    console.error("[data-admin]", err.message);
    return send(res, 400, { error: err.message || "Request failed." });
  }
});
server.listen(PORT, "127.0.0.1", () => {
  console.log(`MedOrbit Data Manager: http://127.0.0.1:${PORT}`);
  console.log("Local-only listener. Use a secure authenticated tunnel for remote access.");
  if (!TOKEN || TOKEN.length < 24) console.warn("Set ADMIN_TOKEN to a random secret of at least 24 characters.");
});
