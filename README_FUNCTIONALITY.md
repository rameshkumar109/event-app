# event-app Application Functionality

This document explains what the application does from a user and system point of view.

## Core Features

- **Event discovery**: Search events by city and aggregate results from multiple sources.
- **Multi‑source aggregation**: Ticketmaster + BookMyShow mock + PredictHQ are combined into one list.
- **User authentication**: Email/password registration and login with JWT tokens.
- **Google OAuth (optional)**: Sign in via Google and receive a JWT token.
- **City suggestions**: Alphabetical city suggestions using a free external API (GeoNames) with fallback.

## User Flow

1. **Login / Register**
   - Users can create an account or sign in.
   - On success, a JWT is stored in `localStorage` as `gt_user_token`.

2. **Events Page**
   - Users search for events by city.
   - Results are shown as cards.

3. **Logout**
   - Clears `gt_user_token` and returns to login.

## API Endpoints (Backend)

Auth:
- `POST /auth/register` → creates user, returns JWT
- `POST /auth/login` → validates user, returns JWT
- `GET /auth/me` → validates JWT, returns user info
- `GET /auth/google` → starts Google OAuth
- `GET /auth/google/callback` → completes OAuth, returns JWT

Events:
- `GET /events?city=<city>&source=all`
- `GET /events/ticketmaster?city=<city>`
- `GET /events/bookmyshow?city=<city>`
- `GET /events/predicthq?city=<city>`

Cities:
- `GET /cities/search?q=<prefix>` → alphabetical suggestions
- `GET /cities` → all cities (cached)
- `GET /cities/regions` → list of regions
- `GET /cities/countries` → list of countries

## External Services Used

- **Ticketmaster API** — event data
- **PredictHQ API** — event data
- **GeoNames API** — city suggestions (free account required)
- **Google OAuth** — optional login provider

## Frontend Pages

- **Login** (`frontend/src/pages/Login.js`)
- **Register** (`frontend/src/pages/Register.js`)
- **Events** (`frontend/src/pages/Events.js`)

## Data Storage

- **Default**: SQLite (`users.db`) for auth data
- **Optional**: PostgreSQL for production usage

## Configuration Summary

Required in `.env` for full functionality:

```
TICKETMASTER_API_KEY=...
PREDICTHQ_API_KEY=...
SECRET_KEY=...
FLASK_SECRET_KEY=...
GEONAMES_USERNAME=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

Notes:
- Do not commit `.env` files to git.
- Google OAuth requires a configured redirect URI:
  `http://127.0.0.1:5000/auth/google/callback`
