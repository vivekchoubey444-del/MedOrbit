const { json } = require("../utils/http");
const { readData } = require("../utils/data");
async function search(req,res,url) {
  const q = (url.searchParams.get("q") || "").trim().slice(0,100);
  if (!q) return json(res,200,{query:"",results:[]});
  const terms = q.toLowerCase();
  const files = ["courses","colleges","universities","jobs","scholarships","services","pages"];
  const results = [];
  for (const file of files) {
    const data = readData(file);
    const rows = Array.isArray(data) ? data : (data.items || []);
    for (const item of rows) {
      const hay = JSON.stringify(item).toLowerCase();
      if (hay.includes(terms)) results.push({
        title:String(item.title || item.name || item.course || "MedOrbit resource"),
        url:String(item.url || item.path || "/pages/resources.html"),
        category:file
      });
      if (results.length >= 30) break;
    }
  }
  json(res,200,{query:q,results});
}
module.exports = {search};
