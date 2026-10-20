# MedOrbit Document Studio
Install: `python -m pip install -r tools/document-studio/requirements.txt`
Run: `python tools/document-studio/app.py`
Open Codespaces port 4170.
API: POST /api/convert, multipart `file` and `format=pdf|html`.
Health: GET /health.
Set MEDORBIT_LOGO_PATH to the actual PNG/JPG logo path if needed.
For public deployment add authentication and use a production WSGI server.
