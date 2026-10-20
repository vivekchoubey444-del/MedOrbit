const http = require("node:http");
const path = require("node:path");
const fs = require("node:fs");
const { URL } = require("node:url");
const { router } = require("./routes/api.routes");
const { securityHeaders } = require("./middleware/security");
const { errorHandler } = require("./middleware/error-handler");

const root = path.resolve(__dirname, "..");
const port = Number(process.env.PORT || 3000);
const mime = {
  ".html":"text/html; charset=utf-8", ".css":"text/css; charset=utf-8",
  ".js":"text/javascript; charset=utf-8", ".json":"application/json; charset=utf-8",
  ".svg":"image/svg+xml", ".png":"image/png", ".jpg":"image/jpeg",
  ".jpeg":"image/jpeg", ".webp":"image/webp", ".ico":"image/x-icon"
};

const server = http.createServer(async (req, res) => {
  securityHeaders(res);
  try {
    const url = new URL(req.url, "http://localhost");
    if (url.pathname.startsWith("/api/")) {
      const handled = await router(req, res, url);
      if (!handled) {
        res.writeHead(404, {"Content-Type":"application/json; charset=utf-8"});
        res.end(JSON.stringify({error:"API route not found"}));
      }
      return;
    }
    if (req.method !== "GET" && req.method !== "HEAD") {
      res.writeHead(405, {"Content-Type":"application/json; charset=utf-8","Allow":"GET, HEAD"});
      res.end(JSON.stringify({error:"Method not allowed"}));
      return;
    }
    let pathname = decodeURIComponent(url.pathname);
    if (pathname === "/") pathname = "/index.html";
    const target = path.resolve(root, "." + pathname);
    if (!target.startsWith(root + path.sep) && target !== root) {
      res.writeHead(403); res.end("Forbidden"); return;
    }
    let stat;
    try { stat = fs.statSync(target); } catch (_) { stat = null; }
    if (!stat || !stat.isFile()) {
      res.writeHead(404, {"Content-Type":"text/html; charset=utf-8"});
      res.end("<!doctype html><title>Not found</title><h1>Page not found</h1><a href='/'>Return home</a>");
      return;
    }
    res.writeHead(200, {"Content-Type":mime[path.extname(target).toLowerCase()] || "application/octet-stream","Cache-Control":"no-cache","X-Content-Type-Options":"nosniff"});
    if (req.method === "HEAD") return res.end();
    fs.createReadStream(target).pipe(res);
  } catch (err) { errorHandler(err, req, res); }
});
server.listen(port, "0.0.0.0", () => console.log(`[MedOrbit] Server listening on ${port}`));
module.exports = {server};
