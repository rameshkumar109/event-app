import os
from urllib.parse import urlparse, parse_qs
import bcrypt
import jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "sqlite:///./users.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_MINUTES = int(os.getenv("JWT_EXP_MINUTES", "60"))

# SQLAlchemy engine: sqlite needs check_same_thread; other DBs (Postgres) do not
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Detect optional schema parameter in the DATABASE_URL (e.g. ?currentSchema=booking_app)
SCHEMA_NAME = None
DB_URL_TO_USE = DATABASE_URL
try:
    parsed = urlparse(DATABASE_URL)
    qs = parse_qs(parsed.query)
    if "currentSchema" in qs:
        SCHEMA_NAME = qs.get("currentSchema", [None])[0]
    # If there are query params, strip them before passing to psycopg2/sqlalchemy
    if parsed.query:
        # rebuild URL without the query component
        from urllib.parse import urlunparse
        DB_URL_TO_USE = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
except Exception:
    SCHEMA_NAME = None

engine = create_engine(DB_URL_TO_USE, connect_args=connect_args)

# If a schema is requested, set the search_path for each new DB connection
if SCHEMA_NAME:
    @event.listens_for(engine, "connect")
    def set_search_path(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute(f"SET search_path TO {SCHEMA_NAME}")
            cursor.close()
        except Exception:
            # best-effort; ignore if it fails
            pass

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    global engine, SessionLocal
    try:
        Base.metadata.create_all(bind=engine)
        return
    except Exception as e:
        # If Postgres connection fails (auth, network), fall back to local sqlite for development
        print(f"Warning: failed to initialize DB at {DATABASE_URL}: {e}")
        try:
            fallback_url = "sqlite:///./users.db"
            print(f"Falling back to local SQLite at {fallback_url}")
            engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
            SessionLocal = sessionmaker(bind=engine)
            Base.metadata.create_all(bind=engine)
            return
        except Exception as e2:
            print(f"Error: failed to create fallback SQLite DB: {e2}")
            raise


def get_user_by_email(email: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email.lower()).first()
        return user
    finally:
        session.close()


def create_user(email: str, password: str):
    session = SessionLocal()
    try:
        existing = session.query(User).filter(User.email == email.lower()).first()
        if existing:
            return None, "User already exists"

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
        user = User(email=email.lower(), password_hash=pw_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user, None
    finally:
        session.close()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode())
    except Exception:
        return False


def create_token_for_user(user):
    payload = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXP_DELTA_MINUTES),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        return None


# Initialize DB on import
init_db()
