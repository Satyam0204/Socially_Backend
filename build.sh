#!/usr/bin/env bash
set -o errexit
cd socialmedia/
poetry lock --no-update
poetry install

python ../socially_backend/manage.py collectstatic --no-input
python ../socially_backend/manage.py migrate