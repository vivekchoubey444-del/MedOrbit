# MedOrbit

Premium education and careers discovery platform using Royal Sapphire and Champagne Gold.

## Requirements
- Node.js 20+
- Python 3 for the site audit

## Run locally
```bash
npm start
```
Open http://localhost:3000.

## Checks
```bash
npm run check
npm test
npm run audit:site
```

## Structure
- `index.html`: master homepage
- `assets/css`: shared design system
- `assets/js`: frontend interactions
- `assets/data`: JSON data sources
- `auth`, `education`, `career`, `pages`: HTML pages
- `backend/routes`: API routing
- `backend/controllers`: request handlers
- `backend/middleware`: HTTP security and request utilities
- `backend/services`: business services
- `backend/utils`: shared utilities
- `backend/validators`: input validation
- `scripts`: Python maintenance and audit scripts
- `tests`: automated tests

## Authentication status
Login and registration are intentionally disabled until a secure identity provider and persistent user store are configured. Do not store plaintext passwords or enable production authentication without password hashing, session management, rate limiting, CSRF protection where applicable, and account recovery controls.

## Data
The JSON files begin as starter datasets. Add only accurate, verified college, course, scholarship and job records. Do not represent placeholder data as live listings.
