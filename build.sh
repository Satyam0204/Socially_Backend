set -o errexit
cd socialmedia/
poetry install
cd ..
cd socially_backend/
python manage.py collectstatic --no-input
python manage.py migrate