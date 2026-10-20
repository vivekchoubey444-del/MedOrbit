const { json } = require("../utils/http");
function health(req,res) {
  json(res,200,{status:"ok",service:"MedOrbit",time:new Date().toISOString()});
}
module.exports = {health};
