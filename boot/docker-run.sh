#!/usr/bin/env sh
set -e

# Activate venv
. /opt/venv/bin/activate

# Enter code dir
cd /code

# Read host/port from env or defaults
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

# Launch Gunicorn with Uvicorn workers, pointing to app.main:app
exec gunicorn \
  -k uvicorn.workers.UvicornWorker \
  -b "${RUN_HOST}:${RUN_PORT}" \
  app.main:app
