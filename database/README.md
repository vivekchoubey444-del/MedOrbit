# Database setup

The starter schema targets PostgreSQL. It creates public catalogue tables only;
it does not create user accounts, store passwords, or enable authentication.

## Apply the initial migration

Back up the database first. Set `DATABASE_URL` in your private environment,
then use a trusted PostgreSQL client:

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/migrations/001_initial_schema.sql
```

Do not put a production connection string in a committed file or paste it into
public logs. Use a managed database secret store.

## Production requirements

- Use a least-privilege application database role.
- Require TLS for remote database connections.
- Use reviewed, versioned migrations and backups.
- Parameterize SQL queries.
- Add an explicit retention and deletion policy before collecting personal data.
- Implement user/authentication tables only alongside a reviewed identity design.
- Never store plaintext passwords, payment-card data, or session secrets.
