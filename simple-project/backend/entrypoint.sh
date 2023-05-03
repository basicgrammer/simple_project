#!/bin/bash

echo "===== Create Database Specification ====="

python manage.py makemigrations platform_app
python manage.py makemigrations auth_app

# Apply database migrations
echo "===== Create Database By specification ====="

python manage.py migrate platform_app
python manage.py migrate auth_app

# Start App Server
echo "=====  RunServer Start ====="
## Dev Version (Runserver)
python manage.py runserver 0.0.0.0:80

## Production Version (Gunicorn)
# gunicorn --workers=4 --bind 0.0.0.0:80 project_core.wsgi:application --access-logfile history/access.log --error-logfile history/error.log
