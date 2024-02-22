#!/bin/bash
# exit on error
set -o errexit
gunicorn web.asgi:application -k uvicorn.workers.UvicornWorker && daphne -b 0.0.0.0 web.asgi:application --port 8001
#gunicorn web.asgi:application -k uvicorn.workers.UvicornWorker