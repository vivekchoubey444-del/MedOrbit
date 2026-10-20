const fs = require("node:fs");
const path = require("node:path");
const base = path.resolve(__dirname,"../../assets/data");
function readData(name) {
  const target = path.join(base,`${name}.json`);
  try { return JSON.parse(fs.readFileSync(target,"utf8")); }
  catch (_) { return []; }
}
module.exports = {readData};
