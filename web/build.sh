#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pygbag game/main.py
python web/manage.py collectstatic --no-input