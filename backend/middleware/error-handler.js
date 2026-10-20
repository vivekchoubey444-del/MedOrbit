function errorHandler(err,req,res) {
  console.error("[MedOrbit]",err && err.message ? err.message : "Unexpected server error");
  if (res.headersSent) return res.destroy();
  res.writeHead(500,{"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"});
  res.end(JSON.stringify({error:"Internal server error"}));
}
module.exports = {errorHandler};
