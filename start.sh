#! /usr/bin/env sh

set -e

MODULE_NAME=${MODULE_NAME:-app}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}
echo "Running Script at: $APP_MODULE"
export GUNICORN_CONF=${GUNICORN_CONF:-gunicorn_conf.py}
echo "Using GUNICORN_CONF"
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
echo "Starting with $WORKER_CLASS Worker Class"


exec gunicorn  -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"