#!/bin/bash

redis-server &
celery -A app.celery_app worker --loglevel=info &
