const http = require("node:http");

const server = http.createServer((req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (req.url === "/api/health") {
    res.writeHead(200);
    res.end(JSON.stringify({ status: "ok", app: "MEDORBIT" }));
    return;
  }
  res.writeHead(404);
  res.end(JSON.stringify({ error: "Not found" }));
});

const port = Number(process.env.PORT || 3000);
server.listen(port, "0.0.0.0", () => {
  console.log(`MEDORBIT API listening on port ${port}`);
});
