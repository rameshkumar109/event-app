#!/usr/bin/env bash
# Simple helper to create Postgres DB and run init SQL
# Usage: ./create_db.sh <database_url>
# Example: ./create_db.sh postgresql://user:pass@localhost:5432/event-app

set -euo pipefail
DB_URL=${1:-}
if [ -z "$DB_URL" ]; then
  echo "Usage: $0 postgresql://user:pass@host:port/dbname"
  exit 1
fi

# psql accepts the URL directly; just run the SQL
# psql does not accept unknown URI query parameters (e.g. ?currentSchema=...).
# If the user provided query params, strip them before calling psql.
PSQL_URL="$DB_URL"
if [[ "$DB_URL" == *"?"* ]]; then
  PSQL_URL="${DB_URL%%\?*}"
  echo "Note: stripping URI query parameters for psql invocation. Using: $PSQL_URL"
fi

psql "$PSQL_URL" -f "$(dirname "$0")/../db/init.sql"

echo "Database initialized."
