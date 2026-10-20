# MedOrbit configuration and deployment

## Local development
1. Install Node.js 20 or newer and Python 3.
2. Copy `.env.example` to `.env` only for local private configuration.
3. Run `npm run check`, `npm test`, `npm run audit:site`, and `npm run validate:config`.
4. Start the application with `npm start`.
5. Open port 3000 in Codespaces.

## Environment variables
- `NODE_ENV`: development, test, or production.
- `PORT`: HTTP port supplied by the host.
- `APP_BASE_URL`: public canonical base URL.
- `DATABASE_URL`: private PostgreSQL connection string, if a database integration is added.
- `DATABASE_SSL`: database TLS setting; configure to match your provider.
- `AUTH_ENABLED`: remains false in this starter.
- `SESSION_SECRET`: never commit it; authentication is not implemented by the starter.

## PostgreSQL
See `database/README.md` and `database/migrations/001_initial_schema.sql`.
The current application reads its catalogue from JSON. The SQL migration is a database foundation, not an automatic JSON-to-PostgreSQL synchronization mechanism.

## GitHub Actions
CI validates syntax, tests, environment settings, JSON data, links and basic secret patterns. CodeQL and Dependabot workflows are also provided. Review dependency versions and workflow permissions regularly.

## Deployment
Render configuration is provided in `render.yaml`. Confirm the host supports the selected runtime and build process before production deployment. For Docker, build with `docker build -t medorbit .` and run with an appropriate port mapping.

## Production checklist
- Configure HTTPS and the canonical public URL.
- Add monitoring, structured logs, backups and a restore drill.
- Integrate a maintained identity provider before enabling accounts.
- Add server-side authorization, rate limits, session protection and audit logging.
- Review privacy, cookie, terms and disclaimer pages with qualified counsel.
- Add verified data sources and a process for removing expired listings.
- Run tests and a security review against the actual deployment.
