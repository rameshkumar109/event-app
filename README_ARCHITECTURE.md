# event-app Architecture Diagram

Below is a high‑level architecture diagram describing how the frontend, backend, and external services interact.

```mermaid
flowchart LR
  subgraph Client
    UI[React Frontend
Login / Register / Events]
    LS[(LocalStorage
JWT Token)]
  end

  subgraph Backend
    API[Flask API]
    AUTH[Auth Service
SQLAlchemy + JWT]
    CITY[City Service]
  end

  subgraph Data
    DB[(SQLite / PostgreSQL
Users DB)]
  end

  subgraph External
    TM[Ticketmaster API]
    PH[PredictHQ API]
    GN[GeoNames API]
    GO[Google OAuth]
  end

  UI -->|/auth/login /auth/register| API
  UI -->|/events?city=...| API
  UI -->|/cities/search?q=...| API

  API --> AUTH --> DB
  API --> CITY --> GN

  API --> TM
  API --> PH

  UI -->|/auth/google| API --> GO
  GO -->|callback| API -->|redirect with JWT| UI

  UI --> LS
```

Notes:
- The frontend stores JWTs in `localStorage` (`gt_user_token`).
- The backend aggregates event data from multiple sources.
- City suggestions are fetched from GeoNames when configured; otherwise fallback data is used.
