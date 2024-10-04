#!/bin/sh

./wait-for-it.sh db:5432 --timeout=30 --strict
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn exhibition_of_kittens.wsgi:application --bind 0.0.0.0:8000