#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
docker-compose up build
python web/manage.py collectstatic --no-input