const path = require("node:path");

function loadConfig(env = process.env) {
  const port = Number(env.PORT || 3000);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }
  const nodeEnv = env.NODE_ENV || "development";
  if (!["development", "test", "production"].includes(nodeEnv)) {
    throw new Error("NODE_ENV must be development, test, or production");
  }
  return Object.freeze({
    nodeEnv,
    port,
    baseUrl: env.APP_BASE_URL || `http://localhost:${port}`,
    dataDirectory: path.resolve(__dirname, "../assets/data"),
    authEnabled: env.AUTH_ENABLED === "true",
    databaseUrlConfigured: Boolean(env.DATABASE_URL),
    logLevel: env.LOG_LEVEL || "info"
  });
}
module.exports = {loadConfig};
