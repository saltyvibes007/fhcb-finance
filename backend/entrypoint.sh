#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput 2>&1 || {
    echo "Migration failed — attempting schema reset and retry..."
    python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')
    db_user = connection.settings_dict.get('USER', 'postgres')
    cursor.execute(f'GRANT ALL ON SCHEMA public TO \"{db_user}\";')
    cursor.execute('GRANT ALL ON SCHEMA public TO PUBLIC;')
print('DB reset.')
"
    python manage.py migrate --noinput
}
echo "Migrations complete."

echo "Provisioning superuser..."
python manage.py createsuperuser --noinput 2>/dev/null || true
echo "Superuser provisioning done."

echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Static files collected."

echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
