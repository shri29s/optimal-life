# Optimal Life — Frontend (React + Vite)

This folder contains a lightweight React frontend scaffold (Vite) for the Optimal Life project.

Quick start

1. Change into the frontend folder:

```bash
cd frontend
```

2. Install dependencies and run the dev server (recommended: pnpm):

```bash
# using pnpm (recommended for speed)
pnpm install
pnpm run dev

# alternative (npm)
# npm install
# npm run dev
```

3. The app will open at `http://localhost:5173` by default. The Vite dev server proxies `/api` to `http://127.0.0.1:8000` (see `vite.config.js`).

Notes

- The React app sends auth requests to `/api/register` and `/api/login`. The dev server rewrites `/api` to the backend address; make sure your FastAPI backend runs on port 8000.
- Tokens are stored in `localStorage` under `access_token` for this prototype.

Next steps / ideas

- Implement a proper router (React Router) and pages for expenses, tasks, habits, etc.
- Use a more secure token store (httpOnly cookies) in production and set `SECRET_KEY` securely.
