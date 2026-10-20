const test = require("node:test");
const assert = require("node:assert/strict");

test("MEDORBIT project manifest is valid", () => {
  const pkg = require("../package.json");
  assert.equal(pkg.name, "medorbit");
  assert.equal(typeof pkg.scripts.start, "string");
});
