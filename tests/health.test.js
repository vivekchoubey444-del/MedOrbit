const test = require("node:test");
const assert = require("node:assert/strict");
test("MedOrbit package is configured", () => {
  const pkg = require("../package.json");
  assert.equal(pkg.name, "medorbit");
  assert.ok(pkg.scripts.start);
});
test("data utility returns an array or object for courses", () => {
  const {readData} = require("../backend/utils/data");
  const courses = readData("courses");
  assert.ok(Array.isArray(courses));
  assert.ok(courses.length >= 1);
});
