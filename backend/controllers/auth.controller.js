const { json } = require("../utils/http");
function authStatus(req,res,url) {
  if (url.pathname === "/api/v1/auth/me" && req.method === "GET") {
    return json(res,401,{error:"Authentication is not configured. Connect a secure identity provider before using accounts."});
  }
  if (["/api/v1/auth/login","/api/v1/auth/register"].includes(url.pathname)) {
    res.setHeader("Allow","GET");
    return json(res,503,{error:"Account authentication is not configured yet. No credentials were stored. Configure a secure identity provider and persistent user store before enabling login or registration."});
  }
  return json(res,404,{error:"Authentication endpoint not found"});
}
module.exports = {authStatus};
