#!/bin/bash

## django entrypoint script

# commom_script_1="python manage.py makemigrations "
# common_script_2="python manage.py migrate "


echo "===== Create Database Specification ====="
# python manage.py makemigrations

python manage.py makemigrations platform_app
python manage.py makemigrations auth_app
# python manage.py makemigrations


# Apply database migrations
echo "===== Create Database By specification ====="
# python manage.py migrate
python manage.py migrate platform_app
python manage.py migrate auth_app
# python manage.py migrate


## OAuth2 migrate
# python manage.py migrate oauth2_provider

# Start App Server
echo "=====  RunServer Start ====="

## Dev Version
python manage.py runserver 0.0.0.0:80


## Product Version
# gunicorn --workers=16 --bind 0.0.0.0:80 project_core.wsgi:application --access-logfile history/access.log --error-logfile history/error.log
# echo "=========== Gunicorn(WSGI) Server Start =============" 
# gunicorn --workers=16 --bind 0.0.0.0:80 project_core.wsgi:application
# gunicorn --workers=16 --bind 0.0.0.0:80 project_core.wsgi:application --access-logfile history/access.log --error-logfile history/error.log

