# Auth database setup (Postgres)

This project ships with a simple auth service using SQLAlchemy. By default it uses SQLite (`sqlite:///./users.db`) for development. To use PostgreSQL for production or dev, follow these steps.

1. Create a PostgreSQL database and user.

   Example using psql:

   ```bash
   sudo -u postgres psql
   CREATE USER gt_user WITH PASSWORD 'strongpassword';
   CREATE DATABASE globoticket;
   GRANT ALL PRIVILEGES ON DATABASE globoticket TO gt_user;
   \q
   ```

2. Initialize schema using the provided script (you can also run the SQL file manually):

   ```bash
   ./scripts/create_db.sh postgresql://gt_user:strongpassword@localhost:5432/globoticket
   ```

3. Set environment variables before starting the backend (prefer `backend/.env`):

   ```bash
   export AUTH_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/globoticket?currentSchema=booking_app"
   export SECRET_KEY="replace-with-strong-secret"
   export JWT_EXP_MINUTES=60
   export FLASK_SECRET_KEY="replace-with-strong-secret"
   ```

4. Start the backend (it will use the provided `AUTH_DATABASE_URL`):

   ```bash
   python3 app.py
   ```

Notes:
- The SQL schema is in `db/init.sql` and creates a `users` table with an email index.
- If you change database URL, ensure `AUTH_DATABASE_URL` is available in the environment where the Flask app runs.
- For production, protect the `SECRET_KEY` and use HTTPS.

Google OAuth (optional):
1. Create OAuth credentials in Google Cloud and add the redirect URL:
   `http://127.0.0.1:5000/auth/google/callback`
2. Set these in `backend/.env`:

   ```bash
   GOOGLE_CLIENT_ID="your_client_id"
   GOOGLE_CLIENT_SECRET="your_client_secret"
   GOOGLE_REDIRECT_URI="http://127.0.0.1:5000/auth/google/callback"
   FRONTEND_URL="http://localhost:3000"
   ```

GeoNames city suggestions (optional):
1. Create a free account at geonames.org and enable web services.
2. Set your username:

   ```bash
   GEONAMES_USERNAME="your_geonames_username"
   ```

Security:
- Do not commit `.env` files. Add `backend/.env` to `.gitignore`.
