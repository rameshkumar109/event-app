# event-app App

event-app is an event discovery web app with a React frontend and a Flask backend. It aggregates events from multiple sources (Ticketmaster, BookMyShow mock, PredictHQ), provides email/password auth, optional Google OAuth, and city suggestions based on external data.

**Quick Start (Dev)**

1. Backend
   ```bash
   pip install -r requirements.txt
   python3 backend/app.py
   ```
   Backend runs at `http://127.0.0.1:5000`.

2. Frontend
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Frontend runs at `http://127.0.0.1:3000`.

**Auth + Database**

- Default auth storage is SQLite (`sqlite:///./users.db`) for development.
- For PostgreSQL setup, see `backend/README_AUTH.md`.

**Environment Variables**

Core:
- `AUTH_DATABASE_URL` — SQLAlchemy DB URL for auth (optional; defaults to SQLite)
- `SECRET_KEY` — JWT secret
- `JWT_EXP_MINUTES` — JWT expiry minutes
- `FLASK_SECRET_KEY` — Flask session secret

APIs:
- `TICKETMASTER_API_KEY` — Ticketmaster key
- `PREDICTHQ_API_KEY` — PredictHQ key
- `GEONAMES_USERNAME` — GeoNames username for live city suggestions (free)

Google OAuth (optional):
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI` (default `http://127.0.0.1:5000/auth/google/callback`)
- `FRONTEND_URL` (default `http://localhost:3000`)

**Key Paths**

- `backend/app.py` — Flask routes and API endpoints
- `backend/auth_service.py` — SQLAlchemy user model + JWT helpers
- `backend/README_AUTH.md` — Postgres + OAuth setup
- `frontend/src/pages/Login.js` — Login UI + Google auth trigger
- `frontend/src/pages/Events.js` — Events page

**Notes**

- Do not commit secrets. Add `backend/.env` to `.gitignore`.
