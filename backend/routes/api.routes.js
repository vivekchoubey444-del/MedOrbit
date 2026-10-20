const { health } = require("../controllers/health.controller");
const { search } = require("../controllers/search.controller");
const { authStatus } = require("../controllers/auth.controller");
const { resources } = require("../controllers/resources.controller");

async function router(req, res, url) {
  const key = `${req.method} ${url.pathname}`;
  if (key === "GET /api/health" || key === "GET /api/v1/health") return health(req,res);
  if (key === "GET /api/v1/search") return search(req,res,url);
  if (key === "GET /api/v1/resources") return resources(req,res,url);
  if (url.pathname.startsWith("/api/v1/auth/")) return authStatus(req,res,url);
  return false;
}
module.exports = {router};
