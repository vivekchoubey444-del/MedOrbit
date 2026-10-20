// Secure authentication is intentionally not enabled by the starter.
// Integrate a maintained identity provider or implement password hashing,
// rate limiting, email verification, session rotation and persistent storage
// before accepting credentials. Never store plaintext passwords.
async function register() {
  throw new Error("Configure a secure identity provider before enabling registration.");
}
async function login() {
  throw new Error("Configure a secure identity provider before enabling login.");
}
module.exports = {register,login};
