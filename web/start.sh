#!/bin/bash
# exit on error
set -o errexit
daphne web.asgi:application --port 8001 && gunicorn web.asgi:application -k uvicorn.workers.UvicornWorker
#gunicorn web.asgi:application -k uvicorn.workers.UvicornWorker