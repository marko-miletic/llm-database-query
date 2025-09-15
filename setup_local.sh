#!/usr/bin/env bash
set -euo pipefail

# Starts docker compose and seeds the Postgres DB with an SQL file (default: test_data/northwind.sql).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"
DEFAULT_SQL_FILE="$ROOT_DIR/test_data/northwind.sql"
SQL_FILE="${1:-$DEFAULT_SQL_FILE}"
CONTAINER_NAME="local-llm-postgres"
COMPOSE_FILE="$ROOT_DIR/docker-compose.yml"

log() { echo "[local] $*"; }
err() { echo "[local][ERROR] $*" >&2; }

# Detect docker compose command
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  err "docker compose not found. Install Docker Desktop or docker-compose."
  exit 1
fi

log "Using compose file: $COMPOSE_FILE"
log "SQL file: $SQL_FILE"

# Bring up services
log "Starting Docker services (detached)..."
"${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" up -d

# Wait for Postgres to be ready inside the container
log "Waiting for Postgres container '$CONTAINER_NAME' to be ready..."
MAX_WAIT=60
SECONDS_WAITED=0
until docker exec "$CONTAINER_NAME" bash -lc 'pg_isready -q -U "$POSTGRES_USER" -d "$POSTGRES_DB"' >/dev/null 2>&1; do
  if (( SECONDS_WAITED >= MAX_WAIT )); then
    err "Postgres did not become ready within ${MAX_WAIT}s."
    # Show last logs to help diagnose
    docker logs --tail 50 "$CONTAINER_NAME" || true
    exit 1
  fi
  sleep 2
  ((SECONDS_WAITED+=2))
  log "... still waiting ($SECONDS_WAITED s)"
done
log "Postgres is ready."

# Copy SQL into the container
TMP_PATH="/tmp/seed.sql"
log "Copying SQL into container: $TMP_PATH"
docker cp "$SQL_FILE" "$CONTAINER_NAME":"$TMP_PATH"

# Execute SQL via psql using container env (POSTGRES_USER/DB/PASSWORD)
log "Seeding database inside container via psql..."
# shellcheck disable=SC2016
docker exec -e PGPASSWORD="$(docker exec "$CONTAINER_NAME" bash -lc 'printf %s "$POSTGRES_PASSWORD"')" \
  "$CONTAINER_NAME" bash -lc 'psql -v ON_ERROR_STOP=1 -q -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f '"$TMP_PATH"''

log "Seeding complete."
