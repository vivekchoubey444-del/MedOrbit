const {validEmail,requiredString} = require("../utils/validation");
function validateRegistration(input) {
  return Boolean(input && validEmail(input.email) && requiredString(input.name,100) &&
    typeof input.password === "string" && input.password.length >= 12 && input.password.length <= 200);
}
module.exports = {validateRegistration};
