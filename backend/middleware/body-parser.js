async function readJson(req, maxBytes=1024*1024) {
  let body="", size=0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > maxBytes) {
      const err = new Error("Request body too large"); err.statusCode=413; throw err;
    }
    body += chunk.toString("utf8");
  }
  if (!body) return {};
  try { return JSON.parse(body); }
  catch (_) { const err = new Error("Invalid JSON body"); err.statusCode=400; throw err; }
}
module.exports = {readJson};
