function requiredString(value,max=200) {
  return typeof value === "string" && value.trim().length > 0 && value.trim().length <= max;
}
function validEmail(value) {
  return typeof value === "string" && value.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}
module.exports = {requiredString,validEmail};
