NeuroPlan — Minimal Prototype

This repository contains a minimal prototype of NeuroPlan: a FastAPI backend with ML module stubs and SQLite storage. The goal is a working baseline you can extend into the full app (React + Tailwind frontend, more features).

Quickstart (Windows cmd):

1. Create a Python virtualenv and activate it:
   python -m venv .venv
   .venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the API server:
   uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

4. Run tests:
   pytest -q

Files added:

- backend/: FastAPI app, models, routers, ML modules
- requirements.txt: Python dependencies
- README.md: this file

Next steps:

- Add React + Tailwind frontend in `frontend/`
- Improve ML training pipelines with user data
- Add UI for insights and charts

If you want, I can now implement the auth and API endpoints and run tests locally. Do you want me to proceed?
