#!/bin/bash
# Startup script that runs migrations and starts the server
set -e

echo "========================================="
echo "Starting Blog Application..."
echo "========================================="

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  WARNING: DATABASE_URL environment variable is not set!"
    echo "⚠️  On Render, you MUST create a PostgreSQL database and connect it to this service."
    echo "⚠️  Using SQLite as fallback (DATA WILL BE LOST ON RESTART/DEPLOY!)"
    echo ""
fi

echo "Checking database connection..."
python manage.py check --database default || {
    echo "❌ Database connection failed!"
    echo "Please ensure DATABASE_URL is set correctly and the database is accessible."
    exit 1
}
echo "✅ Database connection successful!"

echo ""
echo "Running database migrations..."
python manage.py migrate --noinput

echo ""
echo "Creating superuser (if needed)..."
python create_superuser.py || true

echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo ""
echo "========================================="
echo "Starting Gunicorn server..."
echo "========================================="
exec gunicorn KishorelinBlog.wsgi:application

