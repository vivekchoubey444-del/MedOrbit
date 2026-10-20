# MedOrbits Royal Sapphire integration

## Frontend files
- `assets/css/royal-sapphire.css`: shared theme and responsive two-column catalog grid.
- `assets/js/medorbits-global.js`: search, optional JSON catalogs, account-form and document-conversion clients.
- `auth/login.html`, `auth/register.html`, `auth/profile.html`: account UI.
- `pages/document-template.html`: document conversion workspace.

## API contracts expected by the frontend
- `GET /api/v1/search?q=term` -> `{ "results": [{ "title": "...", "description": "...", "url": "/..." }] }`
- `POST /api/v1/auth/login` JSON `{ "email": "...", "password": "..." }`
- `POST /api/v1/auth/register` JSON `{ "name": "...", "email": "...", "password": "..." }`
- `GET /api/v1/auth/me` -> authenticated user profile.
- `POST /api/v1/documents/convert` multipart form with `file` and `template=medorbits-royal-sapphire`; returns the converted file as a downloadable response.

These are frontend integration contracts, not proof that the backend endpoints exist. Implement server-side authentication, password hashing, sessions, authorization, CSRF protection where applicable, rate limits, upload validation, malware scanning where available, conversion libraries, and temporary-file cleanup before production use. Never trust file extensions alone. Do not store uploaded documents or credentials in public folders.

## Shared stylesheet
Existing pages receive the stylesheet and script references. Verify relative URL behavior if deploying the site under a subpath rather than the domain root.
