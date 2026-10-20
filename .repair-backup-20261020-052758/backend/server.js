const http = require("node:http");


const searchHandler = (req, res) => {
  const url = new URL(req.url, "http://localhost");

  if (url.pathname !== "/api/v1/search") return false;

  if (req.method !== "GET") {
    res.writeHead(405, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Method not allowed" }));
    return true;
  }

  const q = (url.searchParams.get("q") || "").trim().slice(0, 120);
  const items = [
    { title: "MBBS Admissions", url: "/education/mbbs.html", keywords: "medical mbbs neet" },
    { title: "BDS Admissions", url: "/education/bds.html", keywords: "dentistry dental bds" },
    { title: "Paramedical Courses", url: "/education/paramedical.html", keywords: "paramedical allied health" },
    { title: "Study Abroad", url: "/pages/study-abroad.html", keywords: "abroad international universities" },
    { title: "Career Guidance", url: "/career/index.html", keywords: "career jobs guidance" }
  ];

  const results = q
    ? items.filter(item =>
        (item.title + " " + item.keywords).toLowerCase().includes(q.toLowerCase())
      ).map(({ title, url }) => ({ title, url }))
    : [];

  res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify({ query: q, results }));
  return true;
};

const server = http.createServer((req, res) => {
  if (searchHandler(req, res)) return;
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
