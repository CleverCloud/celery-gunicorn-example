#!/bin/bash

# Start a local Redis only when no Redis add-on is linked (the add-on exposes
# REDIS_URL). This keeps the example self-contained by default.
if [ -z "$REDIS_URL" ]; then
  redis-server &
fi

# Start the Celery worker that processes the tasks submitted by the web app.
celery -A app.celery_app worker --loglevel=info &
