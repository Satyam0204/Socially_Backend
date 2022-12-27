#!/usr/bin/env bash
set -o errexit


pip install -r ./socially_backend/requirements.txt

python3 ./socially_backend/manage.py collectstatic --no-input
python3 ./socially_backend/manage.py migrate