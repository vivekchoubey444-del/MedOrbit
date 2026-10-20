# MEDORBIT

Multi-language starter platform for web and backend development.

## Requirements
- Node.js 20 or newer
- Python 3 for the Python module
- A Java JDK for the Java module
- A C++ compiler for the C++ module

## Run the API
```bash
npm start
```

Check health:
```bash
curl http://127.0.0.1:3000/api/health
```

## Validate
```bash
npm run check
node --test
python3 backend/python/src/main.py
```

Java and C++ modules are starter examples and require their respective compilers.
Never commit real credentials or `.env` files.
