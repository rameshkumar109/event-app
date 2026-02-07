# GloboTicket Technical Stack

This document summarizes the main technologies and libraries used in the project.

## Frontend

- **React** (CRA) — UI framework
- **JavaScript (ES6+)** — app logic
- **CSS** — custom styling

Key deps (from `frontend/package.json`):
- `react`, `react-dom`, `react-scripts`
- `axios` (API calls)

## Backend

- **Python 3**
- **Flask** — REST API server
- **Flask-CORS** — cross‑origin support
- **SQLAlchemy** — ORM for auth storage
- **bcrypt** — password hashing
- **PyJWT** — JWT auth tokens
- **requests** — outbound HTTP calls

## Data & Storage

- **SQLite** (default dev auth DB)
- **PostgreSQL** (optional production auth DB)

## External APIs

- **Ticketmaster** — events data
- **PredictHQ** — events data
- **GeoNames** — city suggestions
- **Google OAuth** — optional login provider

## Project Structure

- `frontend/` — React app
- `backend/` — Flask app
- `requirements.txt` — Python dependencies

## Runtime

- **Node.js + npm** — frontend dev/build
- **Python venv** — backend dependencies
