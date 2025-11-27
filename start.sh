#!/bin/bash
# Startup script that runs migrations and starts the server
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting server..."
exec gunicorn KishorelinBlog.wsgi:application

