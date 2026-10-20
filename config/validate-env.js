const {loadConfig} = require("./app.config");
function validateEnvironment(env = process.env) {
  const config = loadConfig(env);
  const warnings = [];
  if (config.nodeEnv === "production" && !env.APP_BASE_URL) {
    warnings.push("APP_BASE_URL is not set.");
  }
  if (config.nodeEnv === "production" && env.AUTH_ENABLED === "true") {
    if (!env.DATABASE_URL) throw new Error("AUTH_ENABLED requires DATABASE_URL.");
    if (!env.SESSION_SECRET || env.SESSION_SECRET.length < 32) {
      throw new Error("SESSION_SECRET must contain at least 32 characters.");
    }
    throw new Error("Authentication provider integration must be reviewed before enabling AUTH_ENABLED.");
  }
  if (!env.DATABASE_URL) warnings.push("DATABASE_URL is unset; database features are unavailable.");
  if (env.AUTH_ENABLED !== "true") warnings.push("Authentication is disabled.");
  return {config, warnings};
}
if (require.main === module) {
  try {
    const result = validateEnvironment();
    console.log("MedOrbit environment configuration is valid.");
    result.warnings.forEach(w => console.warn("WARNING:", w));
  } catch (error) {
    console.error("Configuration error:", error.message);
    process.exitCode = 1;
  }
}
module.exports = {validateEnvironment};
