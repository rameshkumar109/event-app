-- Create users table for GloboTicket auth
-- Create application schema if not exists
CREATE SCHEMA IF NOT EXISTS booking_app;

-- Create users table inside booking_app schema
CREATE TABLE IF NOT EXISTS booking_app.users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Index for quick lookup
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON booking_app.users(email);
