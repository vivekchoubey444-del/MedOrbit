const { json } = require("../utils/http");
const { readData } = require("../utils/data");
function resources(req,res,url) {
  const q = (url.searchParams.get("q") || "").toLowerCase().slice(0,100);
  const items = readData("services");
  const rows = Array.isArray(items) ? items : (items.items || []);
  json(res,200,{results:rows.filter(x => !q || JSON.stringify(x).toLowerCase().includes(q))});
}
module.exports = {resources};
